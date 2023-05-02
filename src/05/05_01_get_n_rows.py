import pandas as pd

nrows = 30  # 選取筆數
columns = ['Summary', 'Score']  # 選取欄位
data_path = "../04/data/fine_food_reviews_1k.csv"  

# 讀取 csv 檔案
df = pd.read_csv(data_path, nrows=nrows) 
# 篩選非中立資料
df = df.query('Score != 3')
df['completion'] = df['Score'].apply(lambda x:0 if x < 3 else 1)

# 篩選欄位
df2 = df[columns]
# 修改欄位名稱
df2.columns = ['prompt', 'completion']
# 另存新檔
df2.to_csv('./data/sentiment.csv', index=False)
# print(df2)

