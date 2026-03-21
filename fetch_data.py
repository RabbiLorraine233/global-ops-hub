import urllib.request
import json
import datetime

# 目标：获取海外知名营销/运营社区（Reddit r/marketing）的本周最热讨论
url = "https://www.reddit.com/r/marketing/top.json?limit=5&t=week"
# 伪装成一个正规的机器人，防止被网站拒绝
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Ops Trend Bot)'})

try:
    with urllib.request.urlopen(req) as response:
        # 读取并解析海外网站传回来的数据
        data = json.loads(response.read().decode())
        
        articles = []
        for post in data['data']['children']:
            title = post['data']['title']
            link = "https://www.reddit.com" + post['data']['permalink']
            # 提取前120个字符作为摘要，如果没有正文就用默认提示词
            raw_text = post['data'].get('selftext', '')
            desc = raw_text[:120] + "..." if raw_text else "Click to explore this global marketing insight..."
            
            articles.append({
                "title": title,
                "url": link,
                "description": desc
            })

        # 打上系统自动更新的时间戳
        output = {
            "last_updated": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
            "articles": articles
        }

        # 将整理好的数据写入 data.json 文件
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(output, f, indent=4)
            
        print("Success! Global trends fetched and saved.")

except Exception as e:
    print("Error fetching data:", e)
