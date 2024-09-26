from itertools import islice
import os
import re 
import csv
import time
import random
import requests
from lxml import etree

# 数据处理函数
def process_list_to_string(lst):
    if not lst:
        return ''
    processed = [item.strip() for item in lst]
    if len(processed) == 1:
        result = processed[0]
        # 删除所有空格
        result = result.replace(' ', '')
        return result
    else:
        return '/'.join(processed)

def process_introduction(introduction_parts):
    # 首先，将列表中的所有部分连接成一个字符串，并去除首尾的空白字符
    introduction_text = ''.join(introduction_parts).strip()
    
    # 然后，使用正则表达式替换连续的换行符、回车符或<br>标签为单个空格
    # 此处正则表达式匹配一个或多个连续的换行符(\n+)、回车符(\r+)或<br>标签（考虑可能有空格或属性）
    introduction_cleaned = re.sub(r'\s*<br\s*/?>\s*|\n+|\r+', ' ', introduction_text)
    
    # 最后，去除因替换操作可能产生的多余空格（例如，多个连续空格）
    introduction_final = re.sub(r'\s+', ' ', introduction_cleaned).strip()
    
    return introduction_final

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    'cookie': 'bid=HjkboQBf9jU; _pk_id.100001.4cf6=4810471f7e9a9fd6.1724235109.; __yadk_uid=gsuDqMCFCC7NROil0s8bXrj7cNAxNRfF; ll="108289"; _vwo_uuid_v2=D738724D344F76C4BC224467D954234E9|159042b65f9c531474f7a00fbd081555; __utmc=30149280; __utmc=223695111; dbcl2="283054299:BJfgg04OxlE"; ck=4U6n; push_noty_num=0; push_doumail_num=0; __utmv=30149280.28305; ap_v=0,6.0; __utma=30149280.1223520519.1724235109.1724574037.1724583141.7; __utmz=30149280.1724583141.7.3.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmt=1; __utmb=30149280.2.10.1724583141; __utma=223695111.944462449.1724235109.1724574037.1724583164.7; __utmb=223695111.0.10.1724583164; __utmz=223695111.1724583164.7.3.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/misc/sorry; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1724583164%2C%22https%3A%2F%2Fwww.douban.com%2Fmisc%2Fsorry%3Foriginal-url%3Dhttps%3A%2F%2Fmovie.douban.com%2Fsubject%2F1295644%2Fcomments%3Fstart%3D20%26amp%3Blimit%3D20%26amp%3Bstatus%3DP%26amp%3Bsort%3Dnew_score%22%5D; _pk_ses.100001.4cf6=1'
}

## 创建文件对象
f = open('movie_details1.csv', mode='w', encoding='utf-8', newline="")
csv_write = csv.DictWriter(f, fieldnames=['电影名称', '海报地址', '评分', '评论人数', '类型', '上映日期', '片长', '导演', '主演', '国家/地区', '语言', '简介'])
csv_write.writeheader() # 写入文件头

# # 检查文件是否存在
# file_exists = os.path.isfile('movie_details.csv')
# ## 创建文件对象
# f = open('movie_details.csv', mode='a', encoding='utf-8', newline="")
# csv_write = csv.DictWriter(f, fieldnames=['电影名称', '海报地址', '评分', '评论人数', '类型', '上映日期', '片长', '导演', '主演', '国家/地区', '语言', '简介'])
# # 如果文件不存在，写入文件头
# if not file_exists:
#     csv_write.writeheader()

# 打开 CSV 文件
with open('unique_movies.csv', mode='r', encoding='utf-8') as file:
    # 创建 CSV 阅读器
    reader = csv.DictReader(file)
    
    n = 0

    # 遍历每一行
    # for row in reader:
    # 跳过前19行
    for row in islice(reader, 285, None):
        url = row['URL']
        
        page_text = requests.get(url, headers=headers).text
        # etree解析HTML文档
        tree = etree.HTML(page_text)

        # 电影名称
        movie_name = tree.xpath("//div[@id='content']//span[@property='v:itemreviewed']/text()")
        # 海报地址
        image_src = tree.xpath("//div[@id='mainpic']/a[@class='nbgnbg']/img/@src")
        # 评分
        rating = tree.xpath("//div[@class='rating_self clearfix']/strong/text()")
        # 评论人数
        comment_num = tree.xpath("//div[@class='rating_self clearfix']//a[@class='rating_people']/span/text()")
        # 类型
        types = tree.xpath("//div[@id='info']//span[@property='v:genre']/text()")
        # 上映日期
        release_date = tree.xpath("//div[@id='info']//span[@property='v:initialReleaseDate']/text()")
        # 片长
        duration = tree.xpath("//div[@id='info']//span[@property='v:runtime']/text()")
        # 导演
        director = tree.xpath("//div[@id='info']//a[@rel='v:directedBy']/text()")
        # 主演
        actors = tree.xpath("//div[@id='info']//a[@rel='v:starring']/text()")
        # 国家/地区
        regions = tree.xpath("//span[@class='pl'][contains(text(), '制片国家/地区')]/following-sibling::text()[1]")
        # 语言
        languages = tree.xpath("//span[@class='pl'][contains(text(), '语言')]/following-sibling::text()[1]")
        # 简介
        introduction = tree.xpath("//div[@id='link-report-intra']//span[@property='v:summary']/text()")

        # 处理数据
        data_dict = {
            '电影名称': process_list_to_string(movie_name),
            '海报地址': process_list_to_string(image_src),
            '评分': process_list_to_string(rating),
            '评论人数': process_list_to_string(comment_num),
            '类型': process_list_to_string(types),
            '上映日期': process_list_to_string(release_date),
            '片长': process_list_to_string(duration),
            '导演': process_list_to_string(director),
            '主演': process_list_to_string(actors),
            '国家/地区': process_list_to_string(regions),
            '语言': process_list_to_string(languages),
            '简介': process_introduction(introduction)
        }

        csv_write.writerow(data_dict)

        # 设置睡眠时间间隔，防止频繁访问网站
        time.sleep(random.randint(1, 2))

        n += 1
        print(f'{row["电影名称"]}的详细信息爬取成功----->{n}')

print("---------------")
print("所有电影详细信息爬取成功")
            