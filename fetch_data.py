import urllib.request
import json
import datetime

# 我们换用对开发者极度友好的 DEV 社区 API，抓取全球营销（marketing）最新高赞文章
url = "https://dev.to/api/articles?tag=marketing&per_page=5"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        
        articles = []
        for post in data:
            articles.append({
                "title": post.get("title"),
                "url": post.get("url"),
                "description": post.get("description", "Click to read more about this global trend.")
            })

        output = {
            "last_updated": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
            "articles": articles
        }

        # 生成数据文件
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(output, f, indent=4)
            
        print("Success! Global trends fetched and saved.")

except Exception as e:
    print("Error fetching data:", e)
    # 【高阶技巧】万一网络真断了，生成一个兜底文件，绝不让系统崩溃报 128 错误！
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump({"last_updated": "System Maintenance", "articles": []}, f)
