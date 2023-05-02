from flask import Flask, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('data.html')
    
@app.route('/data')
def get_data():
    data = {
        'name': 'John',
        'age': 30,
        'city': 'New York'
    }
    return jsonify(data)
    

@app.route('/data2')
def index2():
    data = {
        'name': 'John',
        'age': 30,
        'city': 'New York'
    }
    return render_template('data2.html', data=data)

if __name__ == '__main__':
    app.run()