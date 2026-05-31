import pandas as pd
import requests
import chardet

from sqlalchemy import create_engine


class DataImporter:

    @staticmethod
    def detect_encoding(file_path):

        with open(file_path, 'rb') as file:
            result = chardet.detect(file.read())

        return result['encoding']

    @staticmethod
    def csv(file_path):

        encoding = DataImporter.detect_encoding(file_path)

        return pd.read_csv(
            file_path,
            encoding=encoding
        )

    @staticmethod
    def excel(file_path):

        return pd.read_excel(file_path)

    @staticmethod
    def json(file_path):

        return pd.read_json(file_path)

    @staticmethod
    def parquet(file_path):

        return pd.read_parquet(file_path)

    @staticmethod
    def sql(connection_string, query):

        engine = create_engine(connection_string)

        return pd.read_sql(query, engine)

    @staticmethod
    def api(url):

        response = requests.get(url)

        return pd.DataFrame(response.json())