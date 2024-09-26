import pandas as pd

# 读取 CSV 文件
df = pd.read_csv('final_film_review.csv', encoding='utf-8', skipinitialspace=True)  # skipinitialspace=True 用于去除列名和数据值前后的空格

# 定义评分等级到满分10分的转换映射
rating_mapping = {
    '力荐': 9,
    '推荐': 7,
    '还行': 5,
    '较差': 3,
    '很差': 1
}

# 创建一个新的评分列
df['评分'] = df['评分等级'].map(rating_mapping)

# 删除原始的评分等级列（如果需要）
df = df.drop(columns=['评分等级'])

# 保存到新的 CSV 文件
df.to_csv('final_film_review1.csv', index=False, encoding='utf-8')

print('影评评分等级转换评分成功！')