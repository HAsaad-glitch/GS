from flask import jsonify
from flask_appbuilder.api import BaseApi, expose

class ExampleApi(BaseApi):
    resource_name = 'example'

    @expose('/hello', methods=['GET'])
    def hello(self):
        return jsonify({'message': 'Hello, World!'}) 