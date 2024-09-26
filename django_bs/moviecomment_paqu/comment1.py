from itertools import islice
import re 
import csv
import time
import random
import requests
from lxml import etree

def process_comments(comments):
    # 首先，将列表中的所有部分连接成一个字符串，并去除首尾的空白字符
    comments_text = ''.join(comments).strip()
    
    # 然后，使用正则表达式替换连续的换行符、回车符或<br>标签为单个空格
    # 此处正则表达式匹配一个或多个连续的换行符(\n+)、回车符(\r+)或<br>标签（考虑可能有空格或属性）
    comments_cleaned = re.sub(r'\s*<br\s*/?>\s*|\n+|\r+', ' ', comments_text)
    
    # 最后，去除因替换操作可能产生的多余空格（例如，多个连续空格）
    comments_final = re.sub(r'\s+', ' ', comments_cleaned).strip()

    return comments_final

pages = 10

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    'cookie': 'bid=HjkboQBf9jU; _pk_id.100001.4cf6=4810471f7e9a9fd6.1724235109.; __yadk_uid=gsuDqMCFCC7NROil0s8bXrj7cNAxNRfF; ll="108289"; _vwo_uuid_v2=D738724D344F76C4BC224467D954234E9|159042b65f9c531474f7a00fbd081555; __utmc=30149280; __utmc=223695111; dbcl2="283054299:BJfgg04OxlE"; ck=4U6n; push_noty_num=0; push_doumail_num=0; __utmv=30149280.28305; ap_v=0,6.0; __utma=30149280.1223520519.1724235109.1724574037.1724583141.7; __utmz=30149280.1724583141.7.3.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmt=1; __utmb=30149280.2.10.1724583141; __utma=223695111.944462449.1724235109.1724574037.1724583164.7; __utmb=223695111.0.10.1724583164; __utmz=223695111.1724583164.7.3.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/misc/sorry; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1724583164%2C%22https%3A%2F%2Fwww.douban.com%2Fmisc%2Fsorry%3Foriginal-url%3Dhttps%3A%2F%2Fmovie.douban.com%2Fsubject%2F1295644%2Fcomments%3Fstart%3D20%26amp%3Blimit%3D20%26amp%3Bstatus%3DP%26amp%3Bsort%3Dnew_score%22%5D; _pk_ses.100001.4cf6=1'
}

## 创建文件对象
f = open('comment3.csv', mode='w', encoding='utf-8', newline="")
csv_write = csv.DictWriter(f, fieldnames=['电影名称', '评论者', '评分等级', '评论日期', '点赞数', '评论内容'])
csv_write.writeheader() # 写入文件头

# 打开 CSV 文件
with open('unique_movies.csv', mode='r', encoding='utf-8') as file:
    # 创建 CSV 阅读器
    reader = csv.DictReader(file)
    
    # 遍历每一行
    # for row in reader:
    # 跳过前19行
    for row in islice(reader, 758, None):
        # 获取电影的 ID
        movie_id = row['电影ID']
        m = 0
        for i in range(pages):
            url = f'https://movie.douban.com/subject/{movie_id}/comments?&start={i*20}&limit=20&status=P&sort=new_score'
            
            page_text = requests.get(url, headers=headers).text
            # etree解析HTML文档
            tree = etree.HTML(page_text)

            # 获取评论者字段
            reviewer = tree.xpath("//div[@class='comment-item ']//span[@class='comment-info']/a/text()")
            # 获取评分等级字段
            score = tree.xpath("//div[@class='comment-item ']//span[@class='comment-info']/span[2]/@title")
            # 获取评论日期字段
            comment_date = tree.xpath("//div[@class='comment-item ']//span[@class='comment-time ']/text()")
            # 获取点赞数字段
            vote_count = tree.xpath("//div[@class='comment-item ']//span[@class='votes vote-count']/text()")
            # 获取评论内容字段
            comments = tree.xpath("//p[@class=' comment-content']/span/text()")



            # 去除评论日期的换行符及空格
            comment_date = list(map(lambda date: re.sub('\s+', ' ', date), comment_date))  # 去掉换行符制表符
            # comment_date = list(filter(None, comment_date))  # 去掉上一步产生的空元素

            # 由于每页20条评论，故需循环20次依次将获取到的字段值写入文件中
            number = min(20, len(comments))
            for j in range(number):
                m += 1
                data_dict = {'电影名称': row["电影名称"], '评论者': reviewer[j], '评分等级': score[j], '评论日期': comment_date[j], '点赞数': vote_count[j], '评论内容': comments[j]}

                print(f'm={m}-->{data_dict}')
                csv_write.writerow(data_dict)

            # 设置睡眠时间间隔，防止频繁访问网站
            time.sleep(random.randint(1, 2))

        print(f'{row["电影名称"]}的短评爬取成功')

print("---------------")
print("所有评论爬取成功")
            