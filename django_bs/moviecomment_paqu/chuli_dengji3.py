import csv

# 源 CSV 文件路径
source_file_path = 'all_comment1.csv'
# 目标 CSV 文件路径
target_file_path = 'final_comment.csv'

# 有效的评论等级列表
valid_ratings = {"力荐", "推荐", "还行", "较差", "很差"}

def is_valid_rating(rating_str):
    """
    检查评论等级是否为有效的预定义值
    """
    return rating_str in valid_ratings

# 读取源 CSV 文件并过滤评论等级
with open(source_file_path, mode='r', encoding='utf-8') as source_file:
    reader = csv.reader(source_file)
    # 读取表头
    header = next(reader)

    # 找到评论等级列的索引
    rating_index = header.index('评分等级')

    # 用于存储过滤后的行数据
    filtered_rows = []

    for row in reader:
        # 获取评论等级
        rating_str = row[rating_index]
        # 检查评论等级是否有效
        if is_valid_rating(rating_str):
            filtered_rows.append(row)
        else:
            print(f"无效的评论等级: {rating_str}，行被删除")

# 写入到新的 CSV 文件
with open(target_file_path, mode='w', encoding='utf-8', newline='') as target_file:
    writer = csv.writer(target_file)
    # 写入表头
    writer.writerow(header)
    # 写入过滤后的每行数据
    for row in filtered_rows:
        writer.writerow(row)

print('评分等级列成功处理！')