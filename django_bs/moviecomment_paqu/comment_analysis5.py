import pandas as pd
from snownlp import SnowNLP
import jieba

# 停用词文件
stopwords_file = 'stopwords.txt'

# 加载停用词列表
with open(stopwords_file, 'r', encoding='utf-8') as f:
    stopwords = set(line.strip() for line in f.readlines())

# 设定情感分析阈值
THRESHOLD_POSITIVE = 0.5
THRESHOLD_NEGATIVE = 0.3

def remove_stopwords(text):
    """去除文本中的停用词"""
    if not isinstance(text, str):
        text = str(text)  # 确保 text 是字符串
    words = jieba.cut(text)  # 分词
    filtered_words = [word for word in words if word not in stopwords]
    filtered_text = ' '.join(filtered_words)
    return filtered_text

def classify_sentiment(score):
    """根据情感得分分类情感"""
    if score >= THRESHOLD_POSITIVE:
        return '正面'
    elif score <= THRESHOLD_NEGATIVE:
        return '负面'
    else:
        return '中性'

def calculate_percentage(score, total):
    """将情感得分转换为百分比，不进行四舍五入，保留小数点后五位"""
    percentage = (score / total) * 100
    # print(f"得分: {score}, 总得分: {total}, 百分比: {percentage}")
    return float(f"{percentage:.5f}")

def analyze_sentiment(text):
    """分析情感得分"""
    if not text:
        return 0  # 处理空文本
    return SnowNLP(text).sentiments

def main():
    # 读取原始评论数据
    df = pd.read_csv('./短评/final_comment.csv')

    # 确保 '评论内容' 列是字符串类型
    df['评论内容'] = df['评论内容'].astype(str)

    # 去除停用词并添加处理后的文本到数据帧
    df['处理后评论'] = df['评论内容'].apply(lambda x: remove_stopwords(x))

    # 检查处理后的评论是否为空
    if df['处理后评论'].empty:
        print("处理后的评论为空")
        return

    # 进行情感分析并生成新的列
    df['情感得分'] = df['处理后评论'].apply(analyze_sentiment)

    # print(df['情感得分'].describe())

    # 计算总得分和总评论数
    total_score = 1
    df['评分程度'] = df['情感得分'].apply(lambda x: calculate_percentage(x, total_score))

    # 添加新列：划分等级
    df['划分等级'] = df['情感得分'].apply(classify_sentiment)

    # 生成新的 CSV 文件
    df.to_csv('1.csv', index=False, columns=[
        '电影名称', '评论者', '评分等级', '评论日期', '点赞数', '划分等级', '评分程度', '情感得分', '处理后评论', '评论内容'
    ])

if __name__ == '__main__':
    main()
    print('短评情感分析成功！')