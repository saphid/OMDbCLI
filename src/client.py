""" This module handles calling OMDbAPI

    Usage:
        client = OMDbClient(apikey="xxxxxx")

        movie = client.get_movie_by_id(id="tt0086190")

        print(movie.title)

"""
import logging
import sys

from typing import Dict, List, Any, Optional

import requests

from src.models import Movie, Query
from src.config import ConfigManager

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class OMDbClient():
    """ Handles all the calls to OMDbAPI and provides functions for getting and searching movies"""

    def __init__(self, base_url: str = None):
        self.config = ConfigManager()
        self.base_url = base_url if base_url else 'http://www.omdbapi.com/'

    def get_movie(self, query: Query) -> Movie:
        """ Runs the query provided to return the best match movie

        Args:
            query (Query): Query with all the data needed to run the request

        Returns:
            Movie: Movie obj with all the responsed data neatly formatted
        """
        resp_json = self._get(params=query.params)
        return self._from_resp_to_movie(movie_resp=resp_json)

    def search_movies(self, query: Query) -> List[Movie]:
        """ Runs the query provided to return a list of movies

        Args:
            query (Query): Query with all the data needed to run the request

        Returns:
            List[Movie]: List of Movie objs with partial data for each movie
        """
        resp_json = self._get(params=query.params)
        return self._from_resp_to_search(search_resp=resp_json)

    def _get(self, params: Dict[str, Optional[str]], retry: int=10) -> Dict[str, Any]:
        """ Handles a get request to OMDbAPI given a dict of parameters

        Args:
            params (Dict[str, str]): Parameters for OMDbAPI in OMDb format (http://www.omdbapi.com/)
            retry (int): retry count

        Returns:
            Dict[str, Any]: Response from request as a dict
        """
        if not retry:
            print('Too many retries, Please check your api key')
            sys.exit(0)
        params['apikey'] = self.config.api_key
        try:
            resp = requests.get(self.base_url, params=params)
            resp.raise_for_status()
        except requests.exceptions.HTTPError as err:
            logging.debug('HTTPError: %s', err)
            print('Your api key was invalid or not yet activated, Please check email and make sure to type your key correctly')
            self.config.invalidate_key()
            return self._get(params=params, retry=retry-1)

        logging.debug('Get Resp: %s', resp.json())
        return resp.json()

    def _from_resp_to_movie(self, movie_resp: Dict[str, Any]) -> Movie:
        """ Converts the JSON response received from OMDbAPI into a Movie object

        Args:
            movie_resp (Dict): Dict from OMDbAPI JSON movie response

        Returns:
            Movie: Object with all the movies properties completely populated
        """
        movie_resp = {key.lower(): value for key, value in movie_resp.items()}
        movie_resp['item_type'] = movie_resp['type']
        del movie_resp['type']
        return Movie(**movie_resp)

    def _from_resp_to_search(self, search_resp: Dict[str, Any]) -> List[Movie]:
        """ Converts the JSON response received from OMDbAPI into a list of Movie objects

        Args:
            search_resp (Dict[str, Any]): Dict from OMDb JSON search response

        Returns:
            List[Movie]: List of objects with movie properties partially populated
                        (only: Title, Year, imdbID, Type, Poster)
        """
        resp_list: Dict[str, Any] = search_resp.get('Search', {})
        if resp_list:
            results_list = [self._from_resp_to_movie(item) for item in search_resp['Search']]
            return results_list
        else:
            raise KeyError("No search results found")

