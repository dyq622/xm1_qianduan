import pandas as pd
import pymysql
import numpy as np

# 读取 CSV 文件
df = pd.read_csv('final_comment.csv')

# 处理 NaN 值，将其转换为 None 以便数据库能够处理
def sanitize_value(value):
    if isinstance(value, float) and np.isnan(value):
        return None
    return value

# 对 DataFrame 的每列应用 sanitize_value 函数
df = df.apply(lambda x: x.map(sanitize_value) if x.name != 'column_to_exclude' else x)

# 数据库连接信息
connection = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='yjngn293416',
    database='django_bishe',
    port=3306,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

try:
    with connection.cursor() as cursor:
        # 插入数据的 SQL 语句
        insert_sql = """
        INSERT INTO app01_movieshortcomment (movieName, commentPerson, ratingScale, commentDate, starNumber, commentContent)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        # 将 DataFrame 转换为列表格式
        data = df.to_records(index=False).tolist()
        
        # 执行批量插入操作
        cursor.executemany(insert_sql, data)
    
    # 提交事务
    connection.commit()

except pymysql.MySQLError as e:
    print(f"Error: {e}")
    connection.rollback()

finally:
    # 关闭连接
    connection.close()