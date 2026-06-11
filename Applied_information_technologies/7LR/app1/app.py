import os
from flask import Flask

app = Flask(__name__)

PORT = os.getenv('PORT', 8081)
PONG = os.getenv('PONG', 'pong-from-app-1')

# Счётчик запросов
counter = 0

@app.route('/')
def index():
    global counter
    counter += 1
    return f'''
    <!DOCTYPE html>
    <html>
    <head><meta charset="UTF-8"><title>{PONG}</title></head>
    <body style="font-family: Arial; text-align: center; padding: 50px;">
        <h1>{PONG}</h1>
        <p>Счётчик запросов: {counter}</p>
        <p>Порт: {PORT}</p>
        <hr>
        <a href="/ping">/ping</a> | <a href="/info">/info</a>
    </body>
    </html>
    '''

@app.route('/ping')
def ping():
    return f'{PONG}\n'

@app.route('/info')
def info():
    return f'App: {PONG} | Port: {PORT} | Requests: {counter}\n'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(PORT))