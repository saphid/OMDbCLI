""" This module handles all of the CLI arguments and user interface stuff
"""

from typing import Dict, Any

import argparse

from src.query import Query

class OMDbCLI():
    """ This class allows an enduser to provide arguments and receive pretty results
    """
    def __init__(self):
        pass

    def run_parser(self):
        parser = argparse.ArgumentParser(
        description='OMDbCLI: Search movies and get details on them')
        subparsers = parser.add_subparsers()
        search_parser = subparsers.add_parser(
            'search', help='Get a list of movies matching the following critria')
        search_parser.set_defaults(func=self.search)
        get_parser = subparsers.add_parser(
            'get',
            help=
            'Gets the details for the movie best matching the following critria')
        get_parser.set_defaults(func=self.get)
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
            'Will find the movie with this IMDB Id number (Used for: --get only)')
        get_parser.add_argument(
            '--tomato',
            help=
            'Shows the Rotten Tomatoes score with the movie details (Used with: --get only)'
        )
        args = parser.parse_args()
        print(type(args))
        args.func(vars(args))

    def get(self, args: Dict[str, Any]):
        query = self._convert_args_to_params(cmd='get', args=args)

    def search(self, args: Dict[str, Any]):
        query = self._convert_args_to_params(cmd='search', args=args)

    def _convert_args_to_params(self, cmd: str, args: Dict[str,Any]) -> Query:
        """ Converts the arguments from the CLI to a Query object

        Args:
            cmd (str): Command being run. ['get','search]
            args (Dict[str,Any]): Arguments provided. {'title': 'star', 'year': '1999'}

        Returns:
            Query: Query object with all the data needed to run the request
        """
        if cmd == 'get':
            del args['func']
        elif cmd == 'search':
            args['search'] = args.get('title')
            del args['title']
            del args['func']
        return Query(**args)




if __name__ == '__main__':
    cli = OMDbCLI()
    cli.run_parser()
