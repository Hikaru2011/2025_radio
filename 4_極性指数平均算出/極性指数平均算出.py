import pandas as pd

print("処理開始")
print("データ読み込み開始")

df = pd.read_excel(r"\3_極性指数検証\timeline_polarity.xlsx")
df_output = pd.read_csv(r"\output.csv")
radio_mean = tv_mean = shinbun_mean = 0

print("平均算出開始")

for year in range(1923,2025):
    for month in range(1,13):
        if year == 2024 and month == 4: #2024年は4月以降のデータがないため
            break
        
        month_df = df[(df["year"] == year) & (df["month"] == month)]

        #radio
        radio_df = month_df[month_df["type"].str.contains("radio", na=False)]
        if len(radio_df) == 0:
            radio_mean = radio_mean
        else:
            radio_mean = radio_df["polarity"].mean()

        #tv
        tv_df = month_df[month_df["type"].str.contains("tv", na=False)]
        if len(tv_df) == 0:
            tv_mean = tv_mean
        else:
            tv_mean = tv_df["polarity"].mean()

        #newspaper
        shinbun_df = month_df[month_df["type"].str.contains("newspaper", na=False)]
        if len(shinbun_df) == 0:
            shinbun_mean = shinbun_mean
        else:
            shinbun_mean = shinbun_df["polarity"].mean()        

        new_row = pd.DataFrame([{
            "year" : year,
            "month" : month,
            "radio" : radio_mean,
            "tv" : tv_mean,
            "newspaper" : shinbun_mean
        }])

        df_output = pd.concat([df_output, new_row], ignore_index=True)
df_output.to_csv(r"\output.csv")
print("処理終了")