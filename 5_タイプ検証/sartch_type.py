import pandas as pd
import re

df = pd.read_excel(r"\1_txt_exel化\timeline_out.xlsx")
df["type"] = df["type"].astype("object")

words_radio = [    "R1","R2","FM","エフエム","AM","am","ラジオ","ニッポン放送","文化放送","TBSラジオ",
    "J-WAVE","NHKラジオ","bayfm","NACK5","FM802","TOKYOFM","JFN","AFN","NHK第一","NHK第二",
    "ラジオNIKKEI","radiko","Radiko","ラジコ","深夜ラジオ",
    "Podcast","podcast","ポッドキャスト","Spotify Podcast","Apple Podcast",
    "Radiotalk","Voicy",
    "BBC Radio","BBC Sounds","NPR","ABC Radio","CBC Radio","Capital FM",
    "iHeartRadio","SiriusXM"]
words_tv = ["G","E","BS1","BS2","HV","TV","tv","テレビ","地デジ","ブラウン管",
    "ハイビジョン","4K","字幕","ゴールデンタイム","プライムタイム","番組表","視聴率",
    "NHK","NHK総合","Eテレ","日テレ","日本テレビ","フジテレビ","TBS","テレビ朝日","テレ朝",
    "テレビ東京","テレ東","BSフジ","BS日テレ","BS朝日","BSテレ東","BS-TBS",
    "BBC","BBC One","BBC Two","CNN","FOX","CBS","NBC","ABC","HBO","Discovery",
    "National Geographic"]
words_shinbun = ["新聞","times","Times","newspaper","連載",
    "朝日新聞","読売新聞","毎日新聞","産経新聞","日経","日本経済新聞","東京新聞","中日新聞",
    "北海道新聞","西日本新聞","スポニチ","スポーツ報知","日刊スポーツ",
    "夕刊","号外","社説","コラム","見出し","新聞社",
    "The New York Times","NYT","Washington Post","The Guardian","The Times",
    "Wall Street Journal","WSJ","Financial Times","USA Today","Le Monde"]
words_internet = ["インターネット","internet","Internet","SNS","X","Twitter","twitter","YouTube",
    "Google","Instagram","Facebook","Meta","web","ウェブサイト","サーバー","オンライン",
    "ブログ","note","ニコニコ","TikTok","LINE","Discord","Reddit","5ch","2ch","Ameblo",
    "Yahoo","楽天","Amazon","eBay","電子掲示板","公式サイト","ホームページ","VPN",
    "クラウド","検索","ドメイン","URL","ブラウザ","Wi-Fi","光回線","プロバイダ","サイバー",
    "Netflix","Hulu","Disney+","Amazon Prime Video","Prime Video","U-NEXT","dアニメ",
    "Abema","TVer","Tubi","Peacock","Paramount+","HBO Max"]
words_book = ["雑誌","付録","出版","書店","月刊","週刊","テキスト","創刊",
    "芥川","直樹","単行本","文庫本","新書","コミック","図書館","全集","改訂版","増補",
    "同人誌","編集部","著者","帯","初版","重版","書評","装丁","ISBN","出版社","特集号",
    "novel","Novel","paperback","hardcover","Hardcover",
    "Penguin Books","Oxford Press","HarperCollins",
    "bestseller","ebook","Ebook","Kindle","Barnes & Noble"]

for i in df.iterrows():
    new_type = None
    infor = i[1]["infor"]
    index = i[0]

    # radio
    for word_radio in words_radio:
        if word_radio in infor:
            new_type = "radio"
            break
    
    # tv
    for word_tv in words_tv:
        if word_tv in infor:
            if new_type is not None:
                new_type = new_type + ",tv"
            else:
                new_type = "tv"
            break

    # newspaper
    for word_shinbun in words_shinbun:
        if word_shinbun in infor:
            if new_type is not None:
                new_type = new_type + ",newspaper"
            else:
                new_type = "newspaper"
            break
    
    #internet
    for word_internet in words_internet:
        if word_internet in infor:
            if new_type is not None:
                new_type = new_type + ",internet"
            else:
                new_type = "internet"
            break
    
    #book
    for word_book in words_book:
        if word_book in infor:
            if new_type is not None:
                new_type = new_type + ",book"
            else:
                new_type = "book"
            break
    
    df.loc[index, "type"] = new_type


    print("//END No:", index, "|type=", new_type, "//")

print("書き出し中,,,")
df.to_excel(r"\timeline_out.xlsx", index=False)
print("END")
