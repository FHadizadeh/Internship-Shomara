try:
    from flask import Flask
    from flask_restful import Resource, Api, reqparse
    import json
    from es_connection import EsManagement
    import warnings
    from elasticsearch import helpers, Elasticsearch
    import csv
    import time
    from normalize_address import normalize

    warnings.filterwarnings('ignore')
except Exception as e:
    print("Modules Missing {}".format(e))

app = Flask(__name__)
api = Api(app)

# ------------------------------------------------------------------------------------------------------------

NODE_NAME = 'address_index'
es = Elasticsearch([{'host': 'elasticsearch', 'port': 9200}])
# change the host to 'localhost' to run the backend locally

# ------------------------------------------------------------------------------------------------------------


def create_index():
    with open('elasticsearch-config/address_mapping.json', encoding='utf-8') as f:
        address_mapping = json.load(f)

    index_name = NODE_NAME

    es_connection = EsManagement()
    es_connection.clear_index(index_name=index_name)
    es_connection.create_index(index_name=index_name, mapping=address_mapping)

    with open('data/addresses.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        helpers.bulk(es, reader, index=index_name)
    print("Indexing Done!")


"""
{
"wildcard": {
    "title": {
        "value": "{}*".format(self.query)
    }
}
}
"""


# def normalize(address):
#     body = {
#         "analyzer": "EL_address_analyzer",
#         "text": address
#     }
#
#     response = es.indices.analyze(index=NODE_NAME, body=body)
#     res = ''
#     for token in response['tokens']:
#         res += token['token']
#         res += ' '
#
#     return res


class Controller(Resource):
    def __init__(self):
        self.query = parser.parse_args().get("query", None)
        self.baseQuery = {
            "size": 10,
            "query": {
                "bool": {
                    "should": [
                        {"match": {
                            "address": {
                                "query": self.query,
                                "fuzziness": "AUTO",
                                "boost": 1}}},
                        {"match_phrase_prefix": {
                            "address": {
                                "query": self.query,
                                "boost": 1}}}
                    ]
                }
            },
            "collapse": {
                "field": "address.keyword"
            }
        }

    def get(self):
        res = es.search(index=NODE_NAME, body=self.baseQuery)
        addresses = res['hits']['hits']
        res = {'addresses': [normalize(parser.parse_args().get("query", None))]}
        for address in addresses:
            res['addresses'].append(normalize(address['_source']['address']))
        print(res)
        return res


parser = reqparse.RequestParser()
parser.add_argument("query", type=str, required=True, help="query parameter is Required ")

api.add_resource(Controller, '/autocomplete')

if __name__ == '__main__':
    while True:
        try:
            if not es.indices.exists(index=NODE_NAME):
                create_index()
            break
        except Exception as e:
            print("Exception {}".format(e))
            time.sleep(2)

    app.run(debug=True, host='0.0.0.0', port=4000)
