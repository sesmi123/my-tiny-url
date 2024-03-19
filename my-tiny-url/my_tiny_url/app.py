import logging
import sys
from flask import Flask, request
from tiny_url import TinyURL
from tiny_url_controller import TinyURLController

def configure_logging():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    return logger

logger = configure_logging()

app = Flask(__name__)
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