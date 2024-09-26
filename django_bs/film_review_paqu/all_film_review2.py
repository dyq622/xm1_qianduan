import csv

# 源 CSV 文件路径
source_file_path = 'film_review2.csv'
# 目标 CSV 文件路径
target_file_path = 'final_film_review.csv'

# 读取源文件内容并添加到目标文件
with open(source_file_path, mode='r', encoding='utf-8') as source_file:
    reader = csv.reader(source_file)
    # 获取源文件的头部
    header = next(reader)

    with open(target_file_path, mode='a', encoding='utf-8', newline='') as target_file:
        writer = csv.writer(target_file)
        
        # 如果目标文件是空的，先写入头部
        if target_file.tell() == 0:
            writer.writerow(header)

        # 写入源文件的内容
        for row in reader:
            writer.writerow(row)

print('写入成功！')