import logging
import sys
from flask import Flask, abort, jsonify, redirect, request
import validators
from tiny_url import TinyURL

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

@app.route('/hello')
def hello():
    return 'Hello, World!'

@app.route('/create-url', methods=['POST'])
def create_short_url():
    if not request.is_json or 'url' not in request.get_json():
        abort(400, description="Request must be JSON and contain 'url' key.")

    long_url = request.get_json()['url']

    if not validators.url(long_url):
        abort(400, description="The provided 'url' is not valid.")

    short_url = tiny_url.get_short_url(long_url)

    if short_url:
        response = {
            "original": long_url,
            "short_url": short_url
        }
        logger.debug(response)
        return jsonify(response), 200

    short_url = tiny_url.shorten_url(long_url)
    response = {
        "original": long_url,
        "short_url": short_url
    }
    return jsonify(response), 201

@app.route('/<short_url>')
def get_long_url(short_url):
    long_url = tiny_url.get_long_url(short_url)
    if not long_url:
        logger.error(f"No URL found for {request.url}")
        return "No URL found!",500
    logger.info(f"Redirecting to {long_url}")
    return redirect(long_url, code=301)

if __name__ == '__main__':
    app.run(debug=True, port=8000)