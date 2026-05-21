from flask import Flask, render_template, jsonify, request
import random
import string

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    length = int(data.get('length', 12))
    
    # Простая генерация: буквы + цифры + спецсимволы (всё вместе)
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(chars) for _ in range(length))
    
    return jsonify({'password': password})

if __name__ == '__main__':
    app.run(debug=True, port=5000)