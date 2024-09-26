import csv

# 源 CSV 文件路径
source_file_path = 'all_comment.csv'
# 目标 CSV 文件路径
target_file_path = 'all_comment1.csv'

# 读取源 CSV 文件并处理评论内容
with open(source_file_path, mode='r', encoding='utf-8') as source_file:
    reader = csv.reader(source_file)
    # 读取表头
    header = next(reader)

    # 用于存储处理后的行数据
    rows = []

    for row in reader:
        # 处理评论内容中的换行符
        row[-1] = row[-1].replace('\n', '. ').replace('\r', '. ').strip()
        rows.append(row)

# 写入到新的 CSV 文件
with open(target_file_path, mode='w', encoding='utf-8', newline='') as target_file:
    writer = csv.writer(target_file)
    # 写入表头
    writer.writerow(header)
    # 写入处理后的每行数据
    for row in rows:
        writer.writerow(row)

print('CSV 文件已成功处理。')