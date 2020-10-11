""" This module handles all of the CLI arguments and user interface stuff
"""

from typing import Dict, Any

import argparse

from src.models import Query
from src.client import OMDbClient


class OMDbCLI():
    """ This class allows an enduser to provide arguments and receive pretty results
    """
    def __init__(self):
        self.client = OMDbClient(api_key="83c6dc42")

    def run_parser(self):
        """ Handles the cli argument parsing, using two subparsers.
            "get" for getting single movies
            "search" for getting lists of matching movies
        """
        parser = argparse.ArgumentParser(
            description='OMDbCLI: Search movies and get details on them')
        parser.set_defaults(func=self.run)
        subparsers = parser.add_subparsers(title="commands", dest="command")
        search_parser = subparsers.add_parser(
            'search',
            help='Get a list of movies matching the following critria')
        get_parser = subparsers.add_parser(
            'get',
            help=
            'Gets the details for the movie best matching the following critria'
        )
        search_parser.add_argument(
            '--title',
            help=
            'Limits the search to movies with this word in the title. IE: "star" will find Starwars movies (Used with: --search OR --get)'
        )
        search_parser.add_argument(
            '--year',
            help=
            'Limits your search to a particular year. (Used with: --search OR --get)'
        )
        get_parser.add_argument(
            '--title',
            help=
            'Limits the search to movies with this word in the title. IE: "star" will find Starwars movies (Used with: --search OR --get)'
        )
        get_parser.add_argument(
            '--year',
            help=
            'Limits your search to a particular year. (Used with: --search OR --get)'
        )
        get_parser.add_argument(
            '--imdbid',
            help=
            'Will find the movie with this IMDB Id number (Used for: --get only)'
        )
        args = parser.parse_args()
        print(args)
        args.func(vars(args))

    def run(self, args: Dict[str, Any]):
        """ Processes the arguments and requests the results from OMDbAPI

        Args:
            args (Dict[str, Any]): Arguments for finding the movie(s)
        """
        command = args.get('command')
        query = self._convert_args_to_params(args=args)


    def _convert_args_to_params(self, args: Dict[str, Any]) -> Query:
        """ Converts the arguments from the CLI to a Query object

        Args:
            cmd (str): Command being run. ['get','search]
            args (Dict[str,Any]): Arguments provided. {'title': 'star', 'year': '1999'}

        Returns:
            Query: Query object with all the data needed to run the request
        """
        if args.get('command') == 'search':
            args['search'] = args.get('title')
            del args['title']
        del args['func']
        del args['command']
        return Query(**args)


if __name__ == '__main__':
    cli = OMDbCLI()
    cli.run_parser()
