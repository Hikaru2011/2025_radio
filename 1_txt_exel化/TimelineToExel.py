
from datetime import datetime
print(datetime.now(),"に処理が開始")
import re
import pandas as pd
import os

# 元の Excel 読み込み
df = pd.read_excel(r"df\timeline.xlsx")

# 国・放送種類リスト
country_temp = "米|英|独|蘭|豪|加|仏|伊|ソ|中|印|満|占|オーストリア|セイロン|ベルギー|フィンランド|スウェーデン|マラヤ|ルクセンブルク|トルコ|タイ|シンガポール|ノルウェー|ブラジル|南ア|西独|ラオス|東独|南独|比"
radio = "R1|R2"
TV = "T|G|E|BS1|BS2|HV"

# 正規表現パターン（安全版）
pattern = r"^(\d+)\.(\d{{1,2}}|[-])({})\s*(.*)$".format(country_temp)
pattern_jp = r"^(\d+)\.(\d{{1,2}}|[-])(?:({}|{})\s*)?(.*)$".format(radio, TV)
all = 0

for i in range(102):
    year = 1923 + i
    path = os.path.join(r"path", "txt", f"{year}.txt")
    
    with open(path, 'r', encoding='utf-8') as f:
        datalist = f.readlines()
        
        for n in datalist:
            # 行ごとに初期化
            month = day = country = infor = type_ = None
            
            match = re.match(pattern, n)
            match_jp = re.match(pattern_jp, n)
            
            if match:
                month = match.group(1)
                day = match.group(2)
                if day == "-":
                    day = 0

                country = match.group(3)
                infor = match.group(4) or ""

            elif match_jp:
                month = match_jp.group(1)
                day = match_jp.group(2)
                if day == "-":
                    day = 0
                country = "日"
                infor = (match_jp.group(3) or "") + (match_jp.group(4) or "")

            # マッチした場合だけ df に追加
            if month is not None and infor is not None:
                new_row = pd.DataFrame([{
                    "year": int(year),
                    "month": int(month),
                    "day": int(day),
                    "country": country,
                    "infor": infor,
                    "type": type_
                }])
                df = pd.concat([df, new_row], ignore_index=True)

            all = all+1
            print(datetime.now(),"に",year,"/",month,"/",day,"No:",all,"の処理終了")

# Excel 出力
df.to_excel(r"\timeline_out.xlsx", index=False)
print(datetime.now(),"に正常な出力が完了")
print("<処理概要>")
print("1923年から{}年までのtxtデータExel化処理".format(year))
print("出力df先頭:")
print(df.head(10))
print("総件数:",len(df))
print("欠損値数:\n",df.isnull().sum())
print("全処理終了時刻:",datetime.now())