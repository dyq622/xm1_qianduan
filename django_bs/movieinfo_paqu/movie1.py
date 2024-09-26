import csv
import time
import requests

pages = 10

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
  }

# 科幻、惊悚、动作、悬疑、剧情、爱情、恐怖、喜剧、动画
types = [17, 19, 5, 10, 11, 13, 20, 24, 25]

# urls = [
#   "https://movie.douban.com/j/chart/top_list?type=5&interval_id=100%3A90&action=&start=0&limit=20",
#   "https://movie.douban.com/j/chart/top_list?type=17&interval_id=100%3A90&action=&start=0&limit=20"
# ]

# 保存到 CSV 文件
with open('movies.csv', mode='w', newline='', encoding='utf-8') as file:
  writer = csv.writer(file)
  writer.writerow(["电影名称", "上映日期", "评分", "评论人数", "演员", "类型", "国家", "电影ID", "URL"])

  for value in types:
    for i in range(pages):
      url = f"https://movie.douban.com/j/chart/top_list?type={value}&interval_id=100%3A90&action=&start={i*20}&limit=20"

      response = requests.get(url, headers=headers)
      movies_date = response.json()

      for movie in movies_date:
        title = movie["title"]
        release_date = movie["release_date"]
        score = movie["score"]
        vote_count = movie["vote_count"]
        # 前三个演员
        top_actors = movie["actors"][:3]
        actors = ','.join(top_actors)
        types = ','.join(movie["types"])
        regions = ','.join(movie["regions"])
        movieid = movie["id"]
        movie_url = movie["url"]

        writer.writerow([title, release_date, score, vote_count, actors, types, regions, movieid, movie_url])

      print(f'第{i+1}页保存成功')
      time.sleep(5)
    
    print(f'type={value}保存成功')
    time.sleep(5)

print("数据已保存到 'movies.csv' ")
