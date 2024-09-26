import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MultiLabelBinarizer
import numpy as np

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

# Encode user and movie IDs
user_encoder = LabelEncoder()
movieID_encoder = LabelEncoder()
# movie_type_encoder = LabelEncoder()
# actor_encoder = LabelEncoder()
# country_encoder = LabelEncoder()


ratings_df['用户ID'] = user_encoder.fit_transform(ratings_df['用户ID'])
ratings_df['电影ID'] = movieID_encoder.fit_transform(ratings_df['电影ID'])

def preprocess_column_with_embedding(df, column_name):
    # 创建 LabelEncoder 实例
    encoder = LabelEncoder()
    
    # 处理数据：按逗号分割并填充空值
    split_data = df[column_name].str.split(',', expand=True).fillna('')
    
    # 扁平化为一维列表
    flat_list = split_data.values.flatten()
    
    # 清理数据：去除空字符串
    flat_list = [x for x in flat_list if x != '']
    
    # 获取唯一值
    unique_values = pd.Series(flat_list).unique()
    
    # 拟合编码器
    encoder.fit(unique_values)
    
    # 转换每一行
    def transform_row(row):
        # 过滤空字符串并转换
        return encoder.transform(row[row != '']).tolist()
    
    # 使用apply对每一行进行转换
    encoded = split_data.apply(transform_row, axis=1)
    
    # 返回编码后的数据和类别
    return len(encoder.classes_), encoder.classes_.tolist(), encoded

# 模拟输入数据，假设 ratings_df 已定义
num_actors, actor_categories, encoded_actors = preprocess_column_with_embedding(ratings_df, '演员')
num_countries, country_categories, encoded_countries = preprocess_column_with_embedding(ratings_df, '国家')
num_movie_types, movie_type_categories, encoded_movie_types = preprocess_column_with_embedding(ratings_df, '电影类型')

# 打印输出，验证结果
# print(num_actors, actor_categories)
# print(num_countries, country_categories)
# print(num_movie_types, movie_type_categories)

# 对评论人数和评分进行标准化
ratings_df['评论人数标准化'] = (ratings_df['评论人数'] - ratings_df['评论人数'].mean()) / ratings_df['评论人数'].std()
ratings_df['用户评分标准化'] = (ratings_df['用户评分'] - ratings_df['用户评分'].mean()) / ratings_df['用户评分'].std()
ratings_df['用户评分有用数标准化'] = (ratings_df['用户评分有用数'] - ratings_df['用户评分有用数'].mean()) / ratings_df['用户评分有用数'].std()
ratings_df['用户评分无用数标准化'] = (ratings_df['用户评分无用数'] - ratings_df['用户评分无用数'].mean()) / ratings_df['用户评分无用数'].std()

# print(ratings_df.head())


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
        num_reviews = torch.tensor(row['评论人数标准化'], dtype=torch.float)
        normalized_rating = torch.tensor(row['用户评分标准化'], dtype=torch.float)
        useful_ratings = torch.tensor(row['用户评分有用数标准化'], dtype=torch.float)
        useless_ratings = torch.tensor(row['用户评分无用数标准化'], dtype=torch.float)
        movie_rating = torch.tensor(row['电影评分'], dtype=torch.float)

        return user, movie, actor, country, movie_type, num_reviews, normalized_rating, useful_ratings, useless_ratings, movie_rating


train_dataset = MovieRatingsDataset(train_df)
test_dataset = MovieRatingsDataset(test_df)

train_dataloader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_dataloader = DataLoader(test_dataset, batch_size=64, shuffle=False)

# 2. NCF模型定义
class NCF(nn.Module):
    def __init__(self, num_users, num_movies, num_actor_categories, num_country_categories, num_movie_type_categories, embedding_dim, hidden_units):
        super(NCF, self).__init__()
        # 嵌入层
        self.user_embedding = nn.Embedding(num_users, embedding_dim)
        self.movie_embedding = nn.Embedding(num_movies, embedding_dim)
        self.actor_embedding = nn.Embedding(num_actor_categories, embedding_dim)
        self.country_embedding = nn.Embedding(num_country_categories, embedding_dim)
        self.movie_type_embedding = nn.Embedding(num_movie_type_categories, embedding_dim)
        
        # 全连接层（MLP）
        self.fc1 = nn.Linear(embedding_dim * 2 + embedding_dim * 3 + 4, hidden_units[0])  # 嵌入 + 嵌入
        self.fc2 = nn.Linear(hidden_units[0], hidden_units[1])
        self.fc3 = nn.Linear(hidden_units[1], 1)
        
        self.relu = nn.ReLU()
        
    def forward(self, user, movie, actor, country, movie_type, num_reviews, normalized_rating, useful_ratings, useless_ratings):
        user_emb = self.user_embedding(user)  # [64, 20]
        movie_emb = self.movie_embedding(movie)  # [64, 20]
        actor_emb = self.actor_embedding(actor)  # [64, 1363, 20]
        country_emb = self.country_embedding(country)  # [64, 50, 20]
        movie_type_emb = self.movie_type_embedding(movie_type)  # [64, 28, 20]

        # 对 actor_emb, country_emb, movie_type_emb 进行池化
        actor_emb = torch.mean(actor_emb, dim=1)  # [64, 20]
        country_emb = torch.mean(country_emb, dim=1)  # [64, 20]
        movie_type_emb = torch.mean(movie_type_emb, dim=1)  # [64, 20]

        # 确保 num_reviews, normalized_rating, useful_ratings, useless_ratings 是浮点类型
        num_reviews = num_reviews.float()
        normalized_rating = normalized_rating.float()
        useful_ratings = useful_ratings.float()
        useless_ratings = useless_ratings.float()

        # 合并嵌入层的输出
        x = torch.cat([user_emb, movie_emb, actor_emb, country_emb, movie_type_emb,
                    num_reviews.unsqueeze(1),
                    normalized_rating.unsqueeze(1),
                    useful_ratings.unsqueeze(1),
                    useless_ratings.unsqueeze(1)], dim=1)
        

        
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.relu(x)
        x = self.fc3(x)
        
        return x.squeeze()


# 3. 训练模型
def train_model(model, dataloader, epochs=10, lr=0.001):
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    
    for epoch in range(epochs):
        model.train()
        epoch_loss = 0
        for user, movie, actor, country, movie_type, num_reviews, normalized_rating, useful_ratings, useless_ratings, movie_rating in dataloader:
            optimizer.zero_grad()
            output = model(user, movie, actor, country, movie_type, num_reviews, normalized_rating, useful_ratings, useless_ratings)
            loss = criterion(output, movie_rating)
            loss.backward()
            optimizer.step()
            
            epoch_loss += loss.item()
        print(f'Epoch {epoch+1}/{epochs}, Loss: {epoch_loss / len(dataloader)}')


num_users = len(user_encoder.classes_)
num_movies = len(movieID_encoder.classes_)
print(f'Number of unique users: {num_users}')
print(f'Number of unique movies: {num_movies}')
embedding_dim = 20
hidden_units = [64, 32]

# Instantiate the model with the new parameters
model = NCF(num_users, num_movies, num_actors, num_countries, num_movie_types, embedding_dim, hidden_units)

# Train the model
train_model(model, train_dataloader)

# 保存模型
torch.save(model.state_dict(), 'model_weights2.pth')

# 4. 评估模型
def evaluate_model(model, dataloader):
    model.eval()
    with torch.no_grad():
        predictions = []
        targets = []
        for user, movie, actor, country, movie_type, num_reviews, normalized_rating, useful_ratings, useless_ratings, movie_rating in dataloader:
            output = model(user, movie, actor, country, movie_type, num_reviews, normalized_rating, useful_ratings, useless_ratings)
            predictions.extend(output.tolist())
            targets.extend(movie_rating.tolist())
            
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