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
    movie_id = 2  # 替换为实际的电影ID
    predicted_rating = predict_rating(model, user_id, movie_id)
    print(f'Predicted Rating for user {user_id} and movie {movie_id}: {predicted_rating}')