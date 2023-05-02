import pandas as pd

# 電影名稱
movie_list = ['Da Vinci Code', 'Bat Man', 'Brokeback Mountain',
              'Harry Potter', 'Psycho', 'Start Wars', 'Mission Impossible']

# 讀取 sentiment_template.csv
with open('./data/sentiment_template.csv', encoding='utf8') as f:
    text = f.read()
        
# 以sentiment_template.csv為範本，產生多筆資料
df = pd.DataFrame()
for line in text.split('\n'):
    if line == '': continue
    for movie in movie_list:
        list1 = line.split('\t')
        # 將 'the movie' 置換為上述電影名稱
        prompt = list1[1].lower().replace('the movie', movie)
        row = pd.DataFrame({'prompt':prompt, 'completion':list1[0]}, index=[0])
        df = pd.concat((df, row), ignore_index=True)

# 存檔
df.to_csv('./data/sentiment_simple.csv', index=False)
