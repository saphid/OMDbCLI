""" This tests the http client for OMDbAPI
"""
import json

from typing import Dict, List, Any

import pytest
import requests
from src.client import OMDbClient
from src.models import Query
from test_data.test_objects import TestData

API_KEY = 'xxxxx'
BASE_URL = 'http://www.omdbapi.com/'

client = OMDbClient(api_key=API_KEY)

def test_client_created():
    """ Tests creation of client """
    assert client.api_key == API_KEY

@pytest.mark.parametrize('movie_resp', TestData.movies())
def test_get(movie_resp: Dict[str,str], requests_mock):
    """ Tests mocked get requests """
    requests_mock.get(BASE_URL, text=json.dumps(movie_resp))
    params = {'t': movie_resp['Title']}
    assert client._get(params=params) == movie_resp
    
@pytest.mark.parametrize('movie_resp', TestData.movies())
def test_create_movie_object(movie_resp: Dict[str, Any]):
    """ Tests API movie response to movie object transform"""
    movie_obj = client._from_resp_to_movie(movie_resp=movie_resp)
    assert movie_resp['Title'] == movie_obj.title
    assert movie_resp['imdbID'] == movie_obj.imdbid

@pytest.mark.parametrize('search_resp', TestData.searches())
def test_create_search_object(search_resp: Dict[str, Any]):
    """ Tests API search response to movie object transform"""
    search_results = client._from_resp_to_search(search_resp=search_resp)
    assert len(search_results) == 10
    for index, item in enumerate(search_resp["Search"]):
        assert search_results[index].title == item['Title']
        assert search_results[index].year == item['Year']
        assert search_results[index].imdbid == item['imdbID']
        assert search_results[index].item_type == item['Type']
        assert search_results[index].poster == item['Poster']

@pytest.mark.parametrize('movie_id,query,movie_json', TestData.get_queries(query_type='movie'))
def test_get_movie(movie_id: str, query: Query, movie_json: Dict[str, Any], mocker):
    """ Tests the get movie function to with _get mocked out

    Args:
        query_params (Dict[str,str]): Params to make a query object
        movie_json (Dict[str, Any]): expected movie results
        mocker ([type]): Mocker
    """
    mocker.patch('src.client.OMDbClient._get', return_value=movie_json)
    movie = client.get_movie(query=query)
    assert movie.imdbid == movie_id

@pytest.mark.parametrize('movie_ids,query,search_json', TestData.get_queries(query_type='search'))
def test_search_movies(movie_ids: str, query: Query, search_json: Dict[str, Any], mocker):
    """ Tests the get movie function to with _get mocked out

    Args:
        query_params (Dict[str,str]): Params to make a query object
        movie_json (Dict[str, Any]): expected movie results
        mocker ([type]): Mocker
    """
    mocker.patch('src.client.OMDbClient._get', return_value=search_json)
    movies: List = client.search_movies(query=query)
    for index, movie in enumerate(movies):
        assert movie.imdbid == movie_ids[index]




# def test_url(requests_mock):
#     requests_mock.get('http://test.com', text='data')
#     assert 'data' == requests.get('http://test.com').text

# def test_get(requests_mock):
#     requests_mock.get('http://www.omdbapi.com/', text='data')
#     assert 'data' == omdb_get('http://www.omdbapi.com/?i=tt3896198&apikey=83c6dc42')

# def omdb_get(url: str) -> str:
#     return requests.get(url).text

