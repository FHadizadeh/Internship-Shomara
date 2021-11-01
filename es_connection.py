import json
import logging
from typing import Dict

import subprocess
import sys

from elasticsearch import Elasticsearch, helpers
import csv


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


# install('pandas')
# install('Elasticsearch')

logging.shutdown()
# logging.basicConfig(filename="es.log", level=logging.INFO)
logger = logging.getLogger('es')
logger.setLevel(logging.INFO)
fh = logging.FileHandler(logger.name + '.log', mode='w')
fh.setLevel(logging.INFO)
formatter = logging.Formatter(fmt='%(asctime)s\t\t%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
fh.setFormatter(formatter)
logger.addHandler(fh)


class EsManagement:
    def __init__(self):
        self.es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        logger.info(self.es.ping())

    def create_index(self, index_name: str, mapping: Dict) -> None:
        """
        Create an ES index.
        :param index_name: Name of the index.
        :param mapping: Mapping of the index
        """
        logger.info(f"Creating index {index_name} with the following schema: {json.dumps(mapping, indent=2)}")
        print(self.es.indices.create(index=index_name, ignore=400, body=mapping))

    def clear_index(self, index_name: str):
        """
        delete an ES index.
        :param index_name: Name of the index.
        """
        logger.info(f"deleting index {index_name}")
        print(self.es.indices.delete(index=index_name, ignore=[400, 404]))

    def load_csv_into_index(self, path: str, index_name: str) -> None:
        """
        load data to an index from a CSV file.
        :param path: The path to the CSV file.
        :param index_name: Name of the index to which documents should be written.
        """
        with open(path, encoding="utf8") as f:
            reader = csv.DictReader(f)
            rows_num = helpers.bulk(self.es, reader, index=index_name)[0]
            logger.info(f"Writing {rows_num} documents to ES index {index_name}")
