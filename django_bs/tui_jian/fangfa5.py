import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
from torch.utils.data import Dataset, DataLoader
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error

# 1. 数据准备    
# Load data
ratings_df = pd.read_csv('xunlian2.csv')

# 在数据准备阶段，创建电影ID到电影名称的映射字典，创建电影名称到电影ID的映射字典
movie_id_to_name = {}
movie_name_to_id = {}

for index, row in ratings_df.iterrows():
    movie_id = row['电影ID']
    movie_name = row['电影名称']
    if movie_id not in movie_id_to_name:
        movie_id_to_name[movie_id] = movie_name
    if movie_name not in movie_name_to_id:
        movie_name_to_id[movie_name] = movie_id

user_encoder = LabelEncoder()
movieID_encoder = LabelEncoder()

ratings_df['用户ID'] = user_encoder.fit_transform(ratings_df['用户ID'])
ratings_df['电影ID'] = movieID_encoder.fit_transform(ratings_df['电影ID'])

# 处理特征嵌入
def preprocess_column_with_embedding(df, column_name):
    encoder = LabelEncoder()
    split_data = df[column_name].str.split(',', expand=True).fillna('')
    flat_list = split_data.values.flatten()
    flat_list = [x for x in flat_list if x != '']
    unique_values = pd.Series(flat_list).unique()
    encoder.fit(unique_values)
    def transform_row(row):
        return encoder.transform(row[row != '']).tolist()
    
    encoded = split_data.apply(transform_row, axis=1)
    
    return len(encoder.classes_), encoder.classes_.tolist(), encoded

# 假设 ratings_df 已定义
num_actors, actor_categories, encoded_actors = preprocess_column_with_embedding(ratings_df, '演员')
num_countries, country_categories, encoded_countries = preprocess_column_with_embedding(ratings_df, '国家')
num_movie_types, movie_type_categories, encoded_movie_types = preprocess_column_with_embedding(ratings_df, '电影类型')

# Create training and test datasets
train_df = ratings_df.sample(frac=0.8, random_state=1)
test_df = ratings_df.drop(train_df.index)

class MovieRatingsDataset(Dataset):
    def __init__(self, data):
        self.data = data
        self.actor_categories = actor_categories
        self.country_categories = country_categories
        self.movie_type_categories = movie_type_categories

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        row = self.data.iloc[idx]
        user = torch.tensor(row['用户ID'], dtype=torch.long)
        movie = torch.tensor(row['电影ID'], dtype=torch.long)
        actor = torch.tensor([1 if cat in row['演员'].split(',') else 0 for cat in actor_categories], dtype=torch.long)
        country = torch.tensor([1 if cat in row['国家'].split(',') else 0 for cat in country_categories], dtype=torch.long)
        movie_type = torch.tensor([1 if cat in row['电影类型'].split(',') else 0 for cat in movie_type_categories], dtype=torch.long)
        movie_rating = torch.tensor(row['电影评分'], dtype=torch.float)
        return user, movie, actor, country, movie_type, movie_rating

train_dataset = MovieRatingsDataset(train_df)
test_dataset = MovieRatingsDataset(test_df)

train_dataloader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_dataloader = DataLoader(test_dataset, batch_size=64, shuffle=False)

# 基于内容的推荐模型
class ContentBasedModel(nn.Module):
    def __init__(self, num_users, num_movies, num_actor_categories, num_country_categories, num_movie_type_categories, embedding_dim, hidden_units):
        super(ContentBasedModel, self).__init__()
        # 嵌入层
        self.user_embedding = nn.Embedding(num_users, embedding_dim)
        self.movie_embedding = nn.Embedding(num_movies, embedding_dim)
        self.actor_embedding = nn.Embedding(num_actor_categories, embedding_dim)
        self.country_embedding = nn.Embedding(num_country_categories, embedding_dim)
        self.movie_type_embedding = nn.Embedding(num_movie_type_categories, embedding_dim)
        
        # 全连接层（MLP）
        self.fc1 = nn.Linear(embedding_dim * 2 + embedding_dim * 3, hidden_units[0])  # 嵌入 + 嵌入
        self.fc2 = nn.Linear(hidden_units[0], hidden_units[1])
        self.fc3 = nn.Linear(hidden_units[1], 1)
        
        self.relu = nn.ReLU()

    def forward(self, user, movie, actor, country, movie_type):
        # 获取嵌入
        user_emb = self.user_embedding(user)
        movie_emb = self.movie_embedding(movie)
        actor_emb = self.actor_embedding(actor)
        country_emb = self.country_embedding(country)
        movie_type_emb = self.movie_type_embedding(movie_type)
        
        # 对 actor_emb, country_emb, movie_type_emb 进行池化
        actor_emb = torch.mean(actor_emb, dim=1)  # [64, embedding_dim]
        country_emb = torch.mean(country_emb, dim=1)  # [64, embedding_dim]
        movie_type_emb = torch.mean(movie_type_emb, dim=1)  # [64, embedding_dim]

        # 合并嵌入层的输出
        x = torch.cat([user_emb, movie_emb, actor_emb, country_emb, movie_type_emb], dim=1)
        
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.relu(x)
        x = self.fc3(x)
        
        return x.squeeze()
    
def train_model(model, dataloader, epochs=10, lr=0.001):
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    
    for epoch in range(epochs):
        model.train()
        epoch_loss = 0
        for user, movie, actor, country, movie_type, movie_rating in dataloader:
            optimizer.zero_grad()
            output = model(user, movie, actor, country, movie_type)
            loss = criterion(output.squeeze(), movie_rating)
            loss.backward()
            optimizer.step()
            
            epoch_loss += loss.item()
        print(f'Epoch {epoch+1}/{epochs}, Loss: {epoch_loss / len(dataloader)}')

def evaluate_model(model, dataloader):
    model.eval()
    with torch.no_grad():
        predictions = []
        targets = []
        for user, movie, actor, country, movie_type, movie_rating in dataloader:
            output = model(user, movie, actor, country, movie_type)
            predictions.extend(output.squeeze().tolist())
            targets.extend(movie_rating.tolist())
            
        mse = mean_squared_error(targets, predictions)
        print(f'Test MSE: {mse}')

num_users = len(user_encoder.classes_)
num_movies = len(movieID_encoder.classes_)
embedding_dim = 20
hidden_units = [64, 32]

# Instantiate the model with the new parameters
model = ContentBasedModel(num_users, num_movies, num_actors, num_countries, num_movie_types, embedding_dim, hidden_units)

# Train the model
train_model(model, train_dataloader)

# 保存模型
torch.save(model.state_dict(), 'content_based_model_weights.pth')

# Evaluate the model
evaluate_model(model, test_dataloader)