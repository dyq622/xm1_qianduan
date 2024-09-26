import pandas as pd
from textblob import TextBlob

film_review_df = pd.read_csv('xunlian2.csv')

# 对评论进行情感分析
film_review_df['情感分析'] = film_review_df['评论内容'].apply(lambda x: TextBlob(x).sentiment.polarity)

# 打印情感分析结果
print(film_review_df['情感分析'].head())