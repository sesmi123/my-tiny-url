from logger import configure_logging
from flask import Flask, request
from tiny_url import TinyURL
from tiny_url_controller import TinyURLController
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app, version='1.0', title='TinyURL API', description='A simple TinyURL API')
ns = api.namespace('', description='URL operations')
logger = configure_logging(__name__)
tiny_url = TinyURL()
controller = TinyURLController(tiny_url, logger)

@ns.route('/hello')
class HelloResource(Resource):
    def get(self):
        """Return a greeting"""
        return 'Hello, World!'
    

url_model = api.model('URLModel', {
    'url': fields.String(required=True, description='The long URL to be shortened')
})    
@ns.route('/create-url')
class CreateShortURLResource(Resource):
    @api.expect(url_model, validate=True)
    @api.response(200, 'Success')
    @api.response(201, 'Success')
    @api.response(400, 'Validation Error')
    def post(self):
        """Create a short URL"""
        return controller.create_short_url(request.json)


@ns.route('/<short_url>')
@api.doc(params={'short_url': 'The short URL identifier'})
class GetLongURLResource(Resource):
    @api.response(301, 'Redirect')
    @api.response(404, 'URL Not Found')
    def get(self, short_url):
        """Redirect to the long URL"""
        return controller.get_long_url(short_url)


if __name__ == '__main__':
    app.run(debug=True, port=8000)