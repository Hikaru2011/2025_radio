import pandas as pd
from tqdm import tqdm

df = pd.read_excel(r"\2_mecab処理\timeline_mecab.xlsx")
print("dfの読み込み終了")
dic = pd.read_csv(r"\pn_ja.csv", sep=":", encoding="utf-8")
print("dicの読み込み終了")

df["polarity"] = None
drop_indexes = []

px = 100/df.shape[0]
pbar = tqdm(total=100)

print("極性検証開始")

for i in df.iterrows():
    index = i[0]
    target = i[1]["word"]
    
    loc = dic.loc[(dic["word"] == target) | (dic["yomi"] == target), "type"].values
    
    if len(loc) > 0:
        df.loc[index, "polarity"] = loc[0]
    else:
        drop_indexes.append(index)
    
    pbar.set_description(f"\r第{index}行目の処理が終了。")
    pbar.update(px)

df.drop(drop_indexes, inplace=True)
df.to_excel(r"\timeline_polarity.xlsx")