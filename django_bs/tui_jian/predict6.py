import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import LabelEncoder

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

ratings_df = pd.read_csv('xunlian2.csv')
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


num_users = len(user_encoder.classes_)
num_movies = len(movieID_encoder.classes_)
embedding_dim = 20
hidden_units = [64, 32] 
model = ContentBasedModel(num_users, num_movies, num_actors, num_countries, num_movie_types, embedding_dim, hidden_units)

# 加载模型权重，使用 weights_only=True
model.load_state_dict(torch.load('content_based_model_weights.pth', weights_only=True))
model.eval()  # 切换到评估模式

# 获取所有电影的嵌入向量
with torch.no_grad():
    movie_ids = torch.arange(num_movies).long()
    movie_embs = model.movie_embedding(movie_ids).numpy()


def save_similarities_to_csv(movie_embs, movieID_encoder, movie_id_to_name, filename='movie_similarities1.csv'):
    # 计算相似性矩阵
    similarity_matrix = cosine_similarity(movie_embs)
    
    # 获取电影名称
    movie_ids = range(len(movie_id_to_name))
    similar_movie_ids = movieID_encoder.inverse_transform(movie_ids)
    movie_names = [movie_id_to_name[movie_id] for movie_id in similar_movie_ids]

    # 创建一个 DataFrame
    df = pd.DataFrame(similarity_matrix, index=movie_names, columns=movie_names)
    
    # 保存到 CSV 文件
    df.to_csv(filename)
    print(f"相似性矩阵已保存到 {filename}")

save_similarities_to_csv(movie_embs, movieID_encoder, movie_id_to_name)