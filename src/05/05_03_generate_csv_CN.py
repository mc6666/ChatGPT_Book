import pandas as pd

# 電影名稱
movie_list = ['達文西密碼', '蝙蝠俠', '斷背山',
              '哈利波特', '驚魂記', '星際大戰', '不可能的任務']
              
# 讀取 sentiment_template.csv
with open('./data/sentiment_template_CN.csv', encoding='utf8') as f:
    text = f.read()
           
# 以sentiment_template.csv為範本，產生多筆資料
df = pd.DataFrame()
for line in text.split('\n'):
    if line == '': continue
    for movie in movie_list:
        list1 = line.split('\t')
        # 將 '電影' 置換為上述電影名稱
        prompt = list1[1].lower().replace('電影', movie)
        row = pd.DataFrame({'prompt':prompt, 'completion':list1[0]}, index=[0])
        df = pd.concat((df, row), ignore_index=True)

# 存檔
df.to_csv('./data/sentiment_simple_CN.csv', index=False)
