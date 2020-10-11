""" Tests CLI function """

import json

from typing import Dict

import pytest

from src.cli import OMDbCLI
from test_data.test_objects import TestData

cli = OMDbCLI()

# TODO add mocks for sys.argv https://stackoverflow.com/questions/18668947/how-do-i-set-sys-argv-so-i-can-unit-test-it

@pytest.mark.parametrize('args,query_params', TestData.arguments())
def test_args_to_query(args: Dict[str,str], query_params: Dict[str,str]):
    """ Tests the CLI parser to query params conversions

    Args:
        arguments (str)): CLI arguments 'search title="Starwars"'
        query_params (Dict[str,str]): Query object params {'search': 'Starwars'}
    """
    query = cli._convert_args_to_params(args=args)
    assert  query.params == query_params

