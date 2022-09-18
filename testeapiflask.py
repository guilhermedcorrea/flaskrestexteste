from flask import Flask, request, jsonify,make_response
from flask_restx import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix
import json
from functools import wraps


authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}

app = Flask(__name__)
api = Api(app)


a_language = api.model('Language', {'language': fields.String('the language')})

languages = []


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'X-API-KEY' in request.headers:
            token = request.headers['X-API-KEY']
            
        if not token:
            return {'message':'Token nao encontradi'}, 401
        
        if token != 'mytoken':
            return {'message': 'nao deu'}, 401

        print('TOKEN: {}'.format(token))
        return f(*args, **kwargs)
    return decorated



@api.route('/language')
class Language(Resource):

    @api.marshal_with(a_language, envelope='languages')
    def get(self):
   
        return languages, 201, {"X-API-KEY":"mytoken"}
     

    @api.expect(a_language)
    def post(self):
        args = request.json
        response = make_response()
        response.headers["X-API-KEY"] = "mytoken"

        task = {
            'language':args['language'],
            'id':args['id'],
            'X-API-KEY':'mytoken'

        }
     
        new_language = api.payload
        new_language['id'] = len(languages) + 1
        languages.append(task)
  

        return args, 201, {"X-API-KEY":"mytoken"}


if __name__ == '__main__':
    app.run(debug=True)