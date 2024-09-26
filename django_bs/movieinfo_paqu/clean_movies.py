import csv

input_file = 'movies.csv'
output_file = 'unique_movies.csv'

# 使用集合存储唯一的 (第一列值, 第二列值) 组合
unique_combinations = set()

# 使用列表存储最终的唯一行（包括表头）
final_rows = []

# 读取 CSV 文件并处理数据
with open(input_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    # 获取表头
    header = next(reader)
    final_rows.append(header)
    
    # 处理每一行
    for row in reader:
        # 只处理 "演员" 列不为空的行
        if row[4] not in (None, '', 'nan'):
            # 创建第一列和第二列的组合
            key = (row[0], row[1])
            # 如果这个组合不存在于集合中，则添加该行
            if key not in unique_combinations:
                unique_combinations.add(key)
                final_rows.append(row)

# 写入唯一的数据到新的 CSV 文件
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    # 写入去重后的所有行
    writer.writerows(final_rows)