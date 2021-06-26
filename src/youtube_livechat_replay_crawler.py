from bs4 import BeautifulSoup
import os
import json
import requests
import requests_html
from urllib.parse import urlparse, parse_qs
import sys

target_url = input("Input YouTube URL: ")
dict_str = ""
next_url = ""
comment_data = []
session = requests_html.HTMLSession()
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

# まず動画ページにrequestsを実行しhtmlソースを手に入れてlive_chat_replayの先頭のurlを入手
resp = session.get(target_url)
resp.html.render(sleep=3, timeout=50)

resp_date = resp.html.search("回視聴{date} にライブ配信")['date'][-10:]
resp_date = resp_date.replace('/', '-')

for iframe in resp.html.find("iframe"):
    if("live_chat_replay" in iframe.attrs["src"]):
        next_url= "".join(["https://www.youtube.com", iframe.attrs["src"]])


while(1):

    try:
        html = session.get(next_url, headers=headers)
        soup = BeautifulSoup(html.text,"lxml")


        # 次に飛ぶurlのデータがある部分をfind_allで探してsplitで整形
        for scrp in soup.find_all("script"):
            if "window[\"ytInitialData\"]" in scrp.next:
                dict_str = scrp.next.split(" = ", 1)[1]

        # 辞書形式と認識すると簡単にデータを取得できるが, 末尾に邪魔なのがあるので消しておく（「空白2つ + \n + ;」を消す）
        dict_str = dict_str.rstrip("  \n;")
        # 辞書形式に変換
        dics = json.loads(dict_str)

        # "https://www.youtube.com/live_chat_replay?continuation=" + continue_url が次のlive_chat_replayのurl
        continue_url = dics["continuationContents"]["liveChatContinuation"]["continuations"][0]["liveChatReplayContinuationData"]["continuation"]
        next_url = "https://www.youtube.com/live_chat_replay?continuation=" + continue_url
        # dics["continuationContents"]["liveChatContinuation"]["actions"]がコメントデータのリスト。
        for samp in dics["continuationContents"]["liveChatContinuation"]["actions"][1:]:
            #comment_data.append(str(samp)+"\n")
            if 'addChatItemAction' not in samp["replayChatItemAction"]["actions"][0]:
                continue
            if 'liveChatTextMessageRenderer' not in samp["replayChatItemAction"]["actions"][0]["addChatItemAction"]["item"]:
                continue
            str1 = str(samp["replayChatItemAction"]["actions"][0]["addChatItemAction"]["item"]["liveChatTextMessageRenderer"]["message"]["runs"])
            if 'emoji' in str1:
                continue
            str1 = str1.replace('[','').replace('{\'text\': \'','').replace('\'}','').replace(', ','').replace(']','')
            comment_data.append(str(samp["replayChatItemAction"]["actions"][0]["addChatItemAction"]["item"]["liveChatTextMessageRenderer"]["timestampText"]["simpleText"]))
            comment_data.append(","+str1+"\n")

    # next_urlが入手できなくなったら終わり
    except:
        break

# （動画ID）.txt にコメントデータを書き込む
url = urlparse(target_url)
query = parse_qs(url.query)
video_id = query["v"][0]
dir_name = f"./dest/{resp_date}_{video_id}" 

if not os.path.exists(dir_name):
    os.makedirs(dir_name)

with open(f"{dir_name}/all_livechat.txt", mode='w', encoding="utf-8") as f:
    f.writelines(comment_data)