from tqdm import tqdm
import MeCab as mecab
import pandas as pd
import re
import time

def print_red(text):
    print(f"\033[31m{text}\033[0m")
    
def print_green(text):
    print(f"\033[32m{text}\033[0m")

print_red("処理を開始")
start_time = time.perf_counter() #処理時間計測開始
pbar = tqdm(total=100) #処理進捗状況確認用バー表示

df = pd.read_excel(r"\1_txt_exel化\timeline_out.xlsx")
df_output = pd.read_excel(r"\timeline_mecab.xlsx")
px = 100/df.shape[0] #tqdmの1コマ分を計算

tagger = mecab.Tagger()

natto = r"^\S+\s+\S+\s+\S+\s+([^\-\t]+)\s*\S+.+$"
shoyu = r"^(\S+)[^a-zA-Z0-9\s]?\s+.+"


for i in df.iterrows():
    index = i[0]
    infor = i[1]["infor"]
    year = i[1]["year"]
    month = i[1]["month"]
    day = i[1]["day"]
    country = i[1]["country"]
    type = i[1]["type"]

    oic = tagger.parse(infor) #mecabの処理結果をoicに格納
    
    for txt in oic.splitlines(): #mecabの処理結果(oic)を一行づつ出力
        match = re.match(natto, txt)
        match2 = re.match(shoyu, txt)
        
        if match:
            new_row = pd.DataFrame([{
                "year": int(year),
                "month": int(month),
                "day": int(day),
                "country": country or "",
                "type": type or "",
                "word": match.group(1),
            }])
            df_output = pd.concat([df_output, new_row], ignore_index=True)
        elif match2:
            new_row = pd.DataFrame([{
                "year": int(year),
                "month": int(month),
                "day": int(day),
                "country": country or "",
                "type": type or "",
                "word": match2.group(1),
            }])
            df_output = pd.concat([df_output, new_row], ignore_index=True)
    
    now_time = time.perf_counter()
    all_time = now_time-start_time   
    pbar.set_description(f"\r第{index}行目の処理が終了,合計処理時間:{all_time},indexデータ:{year}/{month}/{day}")
    pbar.update(px)

df_output.to_excel(r"\timeline_mecab.xlsx")
pbar.close()