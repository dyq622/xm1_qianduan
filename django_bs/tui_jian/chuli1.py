import pandas as pd

def process_similarity_csv(input_filename='movie_similarities1.csv', output_filename='sorted_movie_similarities1.csv'):
    # 读取相似性矩阵 CSV 文件
    df = pd.read_csv(input_filename, index_col=0)
    
    # 创建一个空的列表，用于存储结果
    results = []
    
    # 遍历每一部电影
    for movie in df.index:
        # 获取当前电影的相似性数据
        similarities = df.loc[movie]
        
        # 过滤掉相似性 <= 0 的电影
        filtered_similarities = similarities[similarities > 0]
        
        # 确保 filtered_similarities 是 Series 对象并排序
        if isinstance(filtered_similarities, pd.Series):
            sorted_similarities = filtered_similarities.sort_values(ascending=False)
        else:
            sorted_similarities = pd.Series()
        
        # 如果没有相似电影，则跳过
        if sorted_similarities.empty:
            continue
        
        # 将相似电影的名称转换为字符串列表
        similar_movies_list = ','.join(sorted_similarities.index)
        
        # 将结果添加到结果列表中
        results.append({
            '电影名称': movie,
            '相似电影列表': similar_movies_list
        })
    
    # 将结果列表转换为 DataFrame
    result_df = pd.DataFrame(results)
    
    # 保存结果到新的 CSV 文件
    result_df.to_csv(output_filename, index=False, encoding='utf-8-sig')
    print(f"处理后的电影相似性数据已保存到 {output_filename}")

# 示例：处理相似性矩阵 CSV 文件
process_similarity_csv()