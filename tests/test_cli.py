""" Tests CLI function """

import json

from typing import Dict

import pytest

from src.cli import OMDbCLI

def read_test_data_from_json(test_data_file):
    """ Loads resp data from file and returns converted json"""
    with open(test_data_file) as jsonfile:
        test_data = json.load(jsonfile)
    return test_data

@pytest.mark.parametrize('arguments,query_params', read_test_data_from_json('test_data/test_data_arguments.json'))
def test_cli_arguments_to_querys(arguments: str, query_params: Dict[str,str]):
    """ Tests the CLI parser to query params conversions

    Args:
        arguments (str)): CLI arguments ' --search="Starwars"'
        query_params (Dict[str,str]): Query object params {'search': 'Starwars'}
    """
    cli = OMDbCLI(arguments=arguments)
    assert cli.query_params == query_params

    