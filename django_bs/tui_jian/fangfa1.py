import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder
import numpy as np

# 1. 数据准备
class MovieRatingsDataset(Dataset):
    def __init__(self, data):
        self.data = data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        row = self.data.iloc[idx]
        user = torch.tensor(row['用户ID'], dtype=torch.long)
        movie = torch.tensor(row['电影ID'], dtype=torch.long)
        rating = torch.tensor(row['电影评分'], dtype=torch.float)
        return user, movie, rating

# Load data
ratings_df = pd.read_csv('xunlian1.csv')

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

# Encode user and movie IDs
user_encoder = LabelEncoder()
movieID_encoder = LabelEncoder()

ratings_df['用户ID'] = user_encoder.fit_transform(ratings_df['用户ID'])
ratings_df['电影ID'] = movieID_encoder.fit_transform(ratings_df['电影ID'])

# Create training and test datasets
train_df = ratings_df.sample(frac=0.8, random_state=1)
test_df = ratings_df.drop(train_df.index)

train_dataset = MovieRatingsDataset(train_df)
test_dataset = MovieRatingsDataset(test_df)

train_dataloader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_dataloader = DataLoader(test_dataset, batch_size=64, shuffle=False)

# 2. NCF模型定义
class NCF(nn.Module):
    def __init__(self, num_users, num_movies, embedding_dim, hidden_units):
        super(NCF, self).__init__()
        self.user_embedding = nn.Embedding(num_users, embedding_dim)
        self.movie_embedding = nn.Embedding(num_movies, embedding_dim)
        
        # MLP layers
        self.fc1 = nn.Linear(embedding_dim * 2, hidden_units[0])
        self.fc2 = nn.Linear(hidden_units[0], hidden_units[1])
        self.fc3 = nn.Linear(hidden_units[1], 1)
        
        self.relu = nn.ReLU()
        
    def forward(self, user, movie):
        user_emb = self.user_embedding(user)
        movie_emb = self.movie_embedding(movie)
        x = torch.cat([user_emb, movie_emb], dim=1)
        
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.relu(x)
        x = self.fc3(x)
        
        return x.squeeze()

# Parameters
num_users = ratings_df['用户ID'].max() + 1
num_movies = ratings_df['电影ID'].max() + 1
embedding_dim = 20
hidden_units = [64, 32]

# Instantiate the model
model = NCF(num_users, num_movies, embedding_dim, hidden_units)

# 3. 训练模型
def train_model(model, dataloader, epochs=10, lr=0.001):
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    
    model.train()
    for epoch in range(epochs):
        epoch_loss = 0
        for user, movie, rating in dataloader:
            optimizer.zero_grad()
            output = model(user, movie)
            loss = criterion(output, rating)
            loss.backward()
            optimizer.step()
            
            epoch_loss += loss.item()
        print(f'Epoch {epoch+1}/{epochs}, Loss: {epoch_loss / len(dataloader)}')

# Train the model
train_model(model, train_dataloader)

# 保存模型
torch.save(model.state_dict(), 'model_weights1.pth')

# 4. 评估模型
def evaluate_model(model, dataloader):
    model.eval()
    with torch.no_grad():
        predictions = []
        targets = []
        for user, movie, rating in dataloader:
            output = model(user, movie)
            predictions.extend(output.tolist())
            targets.extend(rating.tolist())
            
        mse = mean_squared_error(targets, predictions)
        print(f'Test MSE: {mse}')

# Evaluate the model
evaluate_model(model, test_dataloader)

# 1. 计算电影的嵌入表示
def get_movie_embeddings(model, num_movies):
    # 将模型设置为评估模式
    model.eval()
    with torch.no_grad():
        movie_embeddings = []
        for movie_id in range(num_movies):
            movie_id_tensor = torch.tensor([movie_id], dtype=torch.long)
            embedding = model.movie_embedding(movie_id_tensor).numpy()
            movie_embeddings.append(embedding)
        movie_embeddings = np.vstack(movie_embeddings)
    return movie_embeddings

# 2. 计算电影之间的相似性
def calculate_similarity(movie_embeddings):
    similarity_matrix = np.dot(movie_embeddings, movie_embeddings.T)
    norms = np.linalg.norm(movie_embeddings, axis=1)
    similarity_matrix /= norms[:, None]
    similarity_matrix /= norms[None, :]
    return similarity_matrix

# 3. 输出电影名称而不是电影ID
def recommend_similar_movies(model, movie_id, num_movies, movieID_encoder, movie_id_to_name, top_k=5):
    # 获取电影嵌入
    movie_embeddings = get_movie_embeddings(model, num_movies)
    
    # 计算相似性
    similarity_matrix = calculate_similarity(movie_embeddings)
    
    # 获取目标电影的相似性分数
    movie_index = movieID_encoder.transform([movie_id])[0]
    similarity_scores = similarity_matrix[movie_index]
    
    # 获取最相似的电影索引
    similar_movie_indices = similarity_scores.argsort()[-(top_k+1):-1][::-1]
    
    # 获取电影 ID
    similar_movie_ids = movieID_encoder.inverse_transform(similar_movie_indices)
    
    # 使用映射字典查找并输出电影名称
    similar_movie_names = [movie_id_to_name[movie_id] for movie_id in similar_movie_ids]
    return similar_movie_names

def get_movie_id_by_name(movie_name):
    return movie_name_to_id.get(movie_name)

# 示例：为电影 ID 3541415 推荐相似的前 5 部电影，并输出电影名称
input_movie_name = input('请输入一部你喜欢的电影，之后我们将为你推荐5部类似的评分前5的电影。')

movie_id = get_movie_id_by_name(input_movie_name)  # 将电影名称转换为电影 ID
recommended_movies = recommend_similar_movies(model, movie_id, num_movies, movieID_encoder, movie_id_to_name, top_k=5)
print(f"与电影《{input_movie_name}》（ID: {movie_id}）相似的前 5 部电影是: {recommended_movies}")