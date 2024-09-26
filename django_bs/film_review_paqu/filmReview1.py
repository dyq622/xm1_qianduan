from itertools import islice
import re 
import csv
import time
import random
import requests
from lxml import etree

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    'cookie': 'bid=HjkboQBf9jU; _pk_id.100001.4cf6=4810471f7e9a9fd6.1724235109.; __yadk_uid=gsuDqMCFCC7NROil0s8bXrj7cNAxNRfF; ll="108289"; _vwo_uuid_v2=D738724D344F76C4BC224467D954234E9|159042b65f9c531474f7a00fbd081555; __utmc=30149280; __utmc=223695111; dbcl2="283054299:BJfgg04OxlE"; ck=4U6n; push_noty_num=0; push_doumail_num=0; __utmv=30149280.28305; ap_v=0,6.0; __utma=30149280.1223520519.1724235109.1724574037.1724583141.7; __utmz=30149280.1724583141.7.3.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmt=1; __utmb=30149280.2.10.1724583141; __utma=223695111.944462449.1724235109.1724574037.1724583164.7; __utmb=223695111.0.10.1724583164; __utmz=223695111.1724583164.7.3.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/misc/sorry; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1724583164%2C%22https%3A%2F%2Fwww.douban.com%2Fmisc%2Fsorry%3Foriginal-url%3Dhttps%3A%2F%2Fmovie.douban.com%2Fsubject%2F1295644%2Fcomments%3Fstart%3D20%26amp%3Blimit%3D20%26amp%3Bstatus%3DP%26amp%3Bsort%3Dnew_score%22%5D; _pk_ses.100001.4cf6=1'
}

## 创建文件对象
f = open('film_review2.csv', mode='w', encoding='utf-8', newline="")
csv_write = csv.DictWriter(f, fieldnames=['电影名称', '电影ID', '用户名', '用户ID', '评分等级', '评论日期', '有用数', '无用数'])
csv_write.writeheader() # 写入文件头

# 打开 CSV 文件
with open('unique_movies.csv', mode='r', encoding='utf-8') as file:
    # 创建 CSV 阅读器
    reader = csv.DictReader(file)
    
    n = 0

    # 遍历每一行
    # for row in reader:
    # 跳过前19行
    for row in islice(reader, 844, None):
        # 获取电影的 ID
        movie_id = row['电影ID']
        m = 0
        pages = 5
        for i in range(pages):
            url = f'https://movie.douban.com/subject/{movie_id}/reviews?start={i*20}'
            
            page_text = requests.get(url, headers=headers).text
            # etree解析HTML文档
            tree = etree.HTML(page_text)

            # 用户名
            user = tree.xpath("//header[@class='main-hd']//a[@class='name']/text()")
            # 用户ID
            user_id = tree.xpath("//div[@class='main review-item']/@id")
            # 评分等级
            score = tree.xpath("//header[@class='main-hd']//span/@title")
            # 评论日期
            comment_date = tree.xpath("//header[@class='main-hd']//span/text()")
            # 有用数
            useful_number = tree.xpath("//div[@class='action']/a[@class='action-btn up']//span/text()")
            # 无用数
            unuseful_number = tree.xpath("//div[@class='action']//a[@class='action-btn down']/span/text()")

            useful_number = list(map(lambda date: re.sub('\s+', ' ', date), useful_number))  # 去掉换行符制表符
            useful_number = list(filter(None, useful_number))  # 去掉上一步产生的空元素

            unuseful_number = list(map(lambda date: re.sub('\s+', ' ', date), unuseful_number))  # 去掉换行符制表符
            unuseful_number = list(filter(None, unuseful_number))  # 去掉上一步产生的空元素

            # 评论内容
            # comments = tree.xpath("//div[@class='short-content']/text()")

            # 去除评论日期的换行符及空格
            # comment_date = list(map(lambda date: re.sub('\s+', ' ', date), comment_date))  # 去掉换行符制表符
            # comment_date = list(filter(None, comment_date))  # 去掉上一步产生的空元素

            if len(score) < len(user):
                pages += 1
                continue

            # 由于每页20条评论，故需循环20次依次将获取到的字段值写入文件中
            number = min(19, len(user))
            # number = 20
            for j in range(number):
                m += 1
                if useful_number[j] == ' ':
                    useful_number[j] = ' 0 '
                if unuseful_number[j] == ' ':
                    unuseful_number[j] = ' 0 '
                data_dict = {'电影名称': row["电影名称"], '电影ID': row["电影ID"], '用户名': user[j], '用户ID': user_id[j], '评分等级': score[j], '评论日期': comment_date[j], '有用数': useful_number[j], '无用数': unuseful_number[j]}

                print(f'm={m}-->{data_dict}')
                csv_write.writerow(data_dict)

            # 设置睡眠时间间隔，防止频繁访问网站
            time.sleep(random.randint(1, 4))

        n += 1
        print(f'{row["电影名称"]}的短评爬取成功----->{n}')

print("---------------")
print("所有评论爬取成功")
            