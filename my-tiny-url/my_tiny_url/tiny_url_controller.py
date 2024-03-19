from flask import jsonify, abort, redirect
import validators

class TinyURLController:
    def __init__(self, tiny_url, logger):
        self.logger = logger
        self.tiny_url = tiny_url

    def create_short_url(self, request):
        """
        Returns a short url of unique alphanumeric code of length 7, if already existing;
        else creates a new short url and returns it
        """
        if not request.is_json or 'url' not in request.get_json():
            abort(400, description="Request must be JSON and contain 'url' key.")

        long_url = request.get_json()['url']

        if not validators.url(long_url):
            abort(400, description="The provided 'url' is not valid.")

        short_url = self.tiny_url.get_short_url(long_url)

        if short_url:
            response = {
                "original": long_url,
                "short_url": short_url
            }
            self.logger.debug(response)
            return jsonify(response), 200

        short_url = self.tiny_url.shorten_url(long_url)
        response = {
            "original": long_url,
            "short_url": short_url
        }
        return jsonify(response), 201

    def get_long_url(self, request, short_url):
        """
        Redirects to the long url corresponding to the short url if found
        """
        long_url = self.tiny_url.get_long_url(short_url)
        if not long_url:
            self.logger.error(f"No URL found for {request.url}")
            return "No URL found!",500
        self.logger.info(f"Redirecting to {long_url}")
        return redirect(long_url, code=301)
