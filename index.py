from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import json

app = Flask(__name__)
api = Api(app)

class QueryJson(Resource):
    def get(self):
        return json.load(open("data.json"))

api.add_resource(QueryJson, '/query')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5000)
