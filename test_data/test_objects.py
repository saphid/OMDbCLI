""" Test data objects"""

from typing import Union, Dict, List
from uuid import uuid4

import json

from src.models import Query



class TestData():
    """ Contains properties of all the test data needed for our tests"""

    @classmethod
    def movies(cls) -> List:
        """ Returns a list of dictionaries of the movie response"""
        return cls._load_data_from_json(json_file='test_data_movie.json')

    @classmethod
    def searches(cls) -> List:
        """ Returns a list of search results """
        return cls._load_data_from_json(json_file='test_data_search.json')

    @classmethod
    def query_objects(cls, query_file: str) -> List:
        """ Returns a list of Query objects"""
        queries: List = cls._load_data_from_json(json_file=query_file)
        return [[params[0], Query(**params[1])] for params in queries]

    @classmethod
    def get_queries(cls, query_type: str) -> List:
        """ Returns a combine list of movie id, query object, movie json"""
        query_file: str = f'test_data_{query_type}_queries.json'
        json_objs: List = cls.movies() if query_type == 'movie' else cls.searches()
        queries: List = cls.query_objects(query_file=query_file)
        results: List = []
        for index, item in enumerate(queries):
            item.append(json_objs[index])
            results.append(item)
        return results

    @classmethod
    def movie_query_params(cls) -> List:
        """ Returns a list of query params"""
        return cls._load_data_from_json(json_file='test_data_movie_queries.json')

    @classmethod
    def arguments(cls) -> List:
        """ Returns a list of arguments and their resulting queries"""
        return cls._load_data_from_json(json_file='test_data_args.json')

    @classmethod
    def configs(cls) -> List:
        """ Returns a list of api_keys for testing"""
        return [str(uuid4())[-8:] for x in range(10)]

    @staticmethod
    def _load_data_from_json(json_file: str) -> List:
        with open(f'test_data/{json_file}') as jsonfile:
            data = json.load(jsonfile)
        return data
