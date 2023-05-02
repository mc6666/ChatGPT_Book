# 載入套件
import requests
import os, json, sys

# 載入密碼
api_key = os.getenv("OPENAI_API_KEY") 
# 建立 http request 的 header
headers = {"Authorization": "Bearer "+api_key}

# 建立【回應】(completion)任務的函數
def creates_completion(data):
    # 指定使用 json 格式
    headers['Content-Type'] = 'application/json'
    
    # 指定【回應】(completion)的任務
    url = 'https://api.openai.com/v1/completions'
    
    # 送出要求(request)，取得回應
    response = requests.post(url, data=data, headers=headers).json()

    return response
    
if __name__ == '__main__':
    # 設定要求(request)的參數
    data = json.dumps({
      "model": "text-davinci-003", # "gpt-3.5-turbo", 
      "prompt": "hello",
      "n": 1,
      "max_tokens": 20,
      "temperature": 0
    })
    dict1 = creates_completion(data)
    print(dict1['choices'][0]['text'])