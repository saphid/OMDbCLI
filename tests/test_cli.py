""" Tests CLI function """

import json

from typing import Dict

import pytest

from src.cli import OMDbCLI

cli = OMDbCLI()

def read_test_data_from_json(test_data_file):
    """ Loads resp data from file and returns converted json"""
    with open(test_data_file) as jsonfile:
        test_data = json.load(jsonfile)
    return test_data

@pytest.mark.parametrize('cmd,args,query_params', read_test_data_from_json('test_data/test_data_get_arguments.json'))
def test_args_to_query(cmd: str, args: Dict[str,str], query_params: Dict[str,str]):
    """ Tests the CLI parser to query params conversions

    Args:
        arguments (str)): CLI arguments 'search title="Starwars"'
        query_params (Dict[str,str]): Query object params {'search': 'Starwars'}
    """
    query = cli._convert_args_to_params(cmd=cmd, args=args)
    assert  query.params == query_params

