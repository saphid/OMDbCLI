""" This tests the query class object"""

from typing import Dict

import json

import pytest

from src.query import Query

def read_test_data_from_json(test_data_file):
    """ Loads resp data from file and returns converted json"""
    with open(test_data_file) as jsonfile:
        test_data = json.load(jsonfile)
    return test_data

@pytest.mark.parametrize('input_params,expected_output_params', read_test_data_from_json('test_data/test_data_queries.json'))
def test_create_query(input_params: Dict[str,str], expected_output_params: Dict[str,str]):
    """ Tests making query objects and returning OMDbAPI params

    Args:
        input_params (Dict[str,str]): Friendly params {"search": "Starwars"}
        expected_output_params (Dict[str,str]): OMDbAPI params {"s":"Starwars"}
    """
    query = Query(**input_params)
    assert expected_output_params == query.params
