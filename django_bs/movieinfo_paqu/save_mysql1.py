import pandas as pd
import pymysql

# 读取 CSV 文件
df = pd.read_csv('unique_movies.csv')

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
    # 插入数据
    insert_sql = """
    INSERT INTO app01_movieinfo (movieName, releaseInfo, movieScoring, commentNumber, mainActor, movieType, movieCountry, movieID, movieURL)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    data = df.to_records(index=False).tolist()
    with connection.cursor() as cursor:
        cursor.executemany(insert_sql, data)
    connection.commit()

finally:
    # 关闭连接
    connection.close()