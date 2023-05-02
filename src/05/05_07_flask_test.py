from flask import Flask

# 建立 Flask 物件 
app = Flask(__name__)

# 建立路由及其處理函數
@app.route("/")
def index():
    return 'OK'

app.run(debug=True)
