""" This tests the query class object"""

from typing import Dict

import json

import pytest

from src.models import Query
from test_data.test_objects import TestData


@pytest.mark.parametrize('_, input_params,expected_params', TestData.movie_query_params())
def test_create_movie_query(_: str ,input_params: Dict[str,str], expected_params: Dict[str,str]):
    """ Tests making query objects and returning OMDbAPI params

    Args:
        _ (str): Not used in this test
        input_params (Dict[str,str]): Friendly params {"search": "Starwars"}
        expected_output_params (Dict[str,str]): OMDbAPI params {"s":"Starwars"}
    """
    query = Query(**input_params)
    assert expected_params == query.params

@pytest.mark.parametrize('_, input_params,expected_params', TestData.movie_query_params())
def test_create_search_query(_: str ,input_params: Dict[str,str], expected_params: Dict[str,str]):
    """ Tests making query objects and returning OMDbAPI params

    Args:
        _ (str): Not used in this test
        input_params (Dict[str,str]): Friendly params {"search": "Starwars"}
        expected_output_params (Dict[str,str]): OMDbAPI params {"s":"Starwars"}
    """
    query = Query(**input_params)
    assert expected_params == query.params
