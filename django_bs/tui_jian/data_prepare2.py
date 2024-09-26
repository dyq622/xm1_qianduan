import pandas as pd

users_df = pd.read_csv('final_film_review1.csv')
movies_df = pd.read_csv('unique_movies.csv')

users_df['用户评分'] = users_df['评分']
users_df['用户评分有用数'] = users_df['有用数']
users_df['用户评分无用数'] = users_df['无用数']
movies_df['电影评分'] = movies_df['评分']
movies_df['电影类型'] = movies_df['类型']

movies_df = movies_df[['电影ID', '电影名称', '电影评分', '评论人数', '电影类型', '演员', '国家']]
users_df = users_df[['用户名', '用户ID', '电影ID', '用户评分', '用户评分有用数', '用户评分无用数']]

users_movies_df = pd.merge(movies_df, users_df, on='电影ID')
users_movies_df.to_csv('xunlian2.csv', index=False, header=True, encoding='utf-8')

print('数据处理成功！')
