from logger import configure_logging
from flask import Flask, request
from tiny_url import TinyURL
from tiny_url_controller import TinyURLController

app = Flask(__name__)
logger = configure_logging(__name__)
tiny_url = TinyURL()
controller = TinyURLController(tiny_url, logger)

@app.route('/hello')
def hello():
    return 'Hello, World!'

@app.route('/create-url', methods=['POST'])
def create_short_url():
    return controller.create_short_url(request)

@app.route('/<short_url>')
def get_long_url(short_url):
    return controller.get_long_url(request, short_url)

if __name__ == '__main__':
    app.run(debug=True, port=8000)