""" This module handles all of the CLI arguments and user interface stuff"""


from typing import Dict, List, Any
from pprint import pprint

import sys
import argparse
import logging

from src.models import Query, Movie
from src.client import OMDbClient

from tabulate import tabulate

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class OMDbCLI():
    """ This class allows an enduser to provide arguments and receive pretty results
    """
    def __init__(self):
        # self.client = OMDbClient(api_key="83c6dc42")
        self.client = OMDbClient()

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
        args.func(vars(args))

    def run(self, args: Dict[str, Any]):
        """ Processes the arguments and requests the results from OMDbAPI

        Args:
            args (Dict[str, Any]): Arguments for finding the movie(s)
        """
        command = args.get('command')
        query = self._convert_args_to_params(args=args)
        if command == 'get':
            movie: Movie = self.client.get_movie(query=query)
            self.display_movie_details(movie=movie)
        elif command == 'search':
            results: List[Movie] = self.client.search_movies(query=query)
            self.display_search_results(results=results, query=query)
            self.search_prompt(results=results, query=query)

    @staticmethod
    def display_movie_details(movie: Movie) -> None:
        """ Prints out all the details of the movie in a readable manner

        Args:
            movie (Movie): Movie Object with all the movie details
        """
        rt_score = ''.join([rating.get('Value') for rating in movie.ratings if rating.get('Source') == 'Rotten Tomatoes'])
        rt_line = f'Rotten Tomatoes: {rt_score}' if rt_score else 'No Rotten Tomatoes score'
        print(f'Movie:\t{movie.title} ({movie.year}) - {movie.rated} - {rt_line}')
        print(f'Writer(s):\t{movie.writer}\nDirector:\t{movie.director}')
        print(f'Actors:\n\t{movie.actors}')
        print(f'Plot:\n\t{movie.plot}')


    def display_search_results(self, results: List[Movie], query: Query) -> None:
        """ Prints out the current page of search results

        Args:
            results (List[Movie]): A list of movies from the search
            query (Query): The query used to perform the search
        """
        page_start = (int(query.page) - 1) * 10
        for index, movie in enumerate(results[page_start:]):
            item_number = index + 1 + page_start 
            print(f'{item_number})\t {movie.title} ({movie.year})')


    def search_prompt(self, results: List[Movie], query: Query) -> None:
        while True:
            answer = input('Press "Enter" for more, or the item number for details: ')
            if answer in ['quit', 'exit']:
                sys.exit(0)
            if not answer:
                query.next_page()
                results.extend(self.client.search_movies(query=query))
                self.display_search_results(results=results, query=query)
                continue
            try:
                item_number = int(answer)
            except ValueError:
                print('Numbers only please')
                continue
            if item_number < int(query.page)*10:
                movie_query = Query(imdbid=results[int(answer)].imdbid)
                found_movie: Movie = self.client.get_movie(query=movie_query)
                self.display_movie_details(movie=found_movie)
                _ = input('Press "Enter" to go back to the search results')
                self.display_search_results(results=results, query=query)



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
    try:
        cli = OMDbCLI()
        cli.run_parser()
    except KeyboardInterrupt:
        sys.exit(0)