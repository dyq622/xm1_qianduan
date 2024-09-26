# predict.py

import torch
from fangfa3 import NCF  # 确保你替换为模型所在的实际文件名

# 定义预测函数
def predict_rating(model, user_id, movie_id):
    user = torch.tensor([user_id], dtype=torch.long)
    movie = torch.tensor([movie_id], dtype=torch.long)
    
    model.eval()
    with torch.no_grad():
        prediction = model(user, movie)
        return prediction.item()

def predict_all_movies(model, user_id, num_movies):
    ratings = []
    for movie_id in range(num_movies):
        rating = predict_rating(model, user_id, movie_id)
        ratings.append((movie_id, rating))
    return ratings

def get_top_n_movies(ratings, n=5):
    # 按照评分排序并取前n个
    return sorted(ratings, key=lambda x: x[1], reverse=True)[:n]

# 示例预测
if __name__ == "__main__":
    # 加载模型（确保加载训练好的模型权重）
    num_users = 34494  # 替换为实际的用户数量
    num_movies = 712  # 替换为实际的电影数量
    embedding_dim = 20
    hidden_units = [64, 32]
    
    model = NCF(num_users, num_movies, embedding_dim, hidden_units)
    model.load_state_dict(torch.load('model_weights.pth', weights_only=False))  # 替换为实际模型权重文件名

    user_id = 1  # 替换为实际的用户ID

    # 为用户预测所有电影的评分
    ratings = predict_all_movies(model, user_id, num_movies)

    # 获取评分最高的5部电影
    top_movies = get_top_n_movies(ratings, n=5)

    # 打印评分最高的5部电影
    print(f'Top 5 movies predicted for user {user_id}:')
    for movie_id, rating in top_movies:
        print(f'Movie ID: {movie_id}, Predicted Rating: {rating:.4f}')