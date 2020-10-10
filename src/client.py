""" This module handles calling OMDbAPI

    Usage:
        client = OMDbClient(apikey="xxxxxx")

        movie = client.get_movie_by_id(id="tt0086190")

        print(movie.title)

"""
from typing import Dict, List, Any

import requests

from src.movie import Movie

class OMDbClient():
    """ Handles all the calls to OMDbAPI and provides functions for getting and searching movies"""

    def __init__(self, api_key: str, base_url: str = None):
        self.api_key = api_key
        self.base_url = base_url if base_url else 'http://www.omdbapi.com/'

    def _get(self, params: Dict[str, str]) -> Dict[str, Any]:
        """ Handles a get request to OMDbAPI given a dict of parameters

        Args:
            params (Dict[str, str]): Parameters for OMDbAPI in OMDb format (http://www.omdbapi.com/)

        Returns:
            Dict[str, Any]: Response from request as a dict
        """
        params['apikey'] = self.api_key
        resp = requests.get(self.base_url, params=params)
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

