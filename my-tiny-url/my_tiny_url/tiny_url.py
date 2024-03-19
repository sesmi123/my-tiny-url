import random
import string

class TinyURL:
    def __init__(self):
        self.url_to_code = {}
        self.code_to_url = {}
        self.base_url = "http://localhost:8000/"
    
    def get_short_url(self, long_url:str):
        """Get existing shortened URL."""
        if long_url in self.url_to_code:
            code = self.url_to_code[long_url]
            return self.base_url + code
        return None

    def shorten_url(self, long_url:str):
        """Encodes a URL to a shortened URL."""
        existing_url = self.get_short_url(long_url)
        if existing_url:
            return existing_url
        
        code = self._generate_code()
        while code in self.code_to_url:
            code = self._generate_code()
        self.url_to_code[long_url] = code
        self.code_to_url[code] = long_url
        return self.base_url + code
    
    def get_long_url(self, short_url):
        """Decodes a shortened URL to its original URL."""
        code = short_url.split('/')[-1]
        if code in self.code_to_url:
            return self.code_to_url[code]
        else:
            return None
    
    def _generate_code(self, length=7):
        """Generates a random code for the short URL."""
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))
