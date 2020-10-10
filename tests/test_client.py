""" This tests the http client for OMDbAPI
"""
import json

from typing import Dict, Any

import pytest
import requests
from src.client import OMDbClient

API_KEY = 'xxxxx'
BASE_URL = 'http://www.omdbapi.com/'

client = OMDbClient(api_key=API_KEY)

def read_test_data_from_json(test_data_file):
    """ Loads resp data from file and returns converted json"""
    with open(test_data_file) as jsonfile:
        test_data = json.load(jsonfile)
    return test_data


def test_client_created():
    """ Tests creation of client """
    assert client.api_key == API_KEY

@pytest.mark.parametrize('movie_resp', read_test_data_from_json('test_data/test_data_movies.json'))
def test_get(movie_resp: Dict[str,str], requests_mock):
    """ Tests mocked get requests """
    requests_mock.get(BASE_URL, text=json.dumps(movie_resp))
    params = {'t': movie_resp['Title']}
    assert client._get(params=params) == movie_resp
    
@pytest.mark.parametrize('movie_resp', read_test_data_from_json('test_data/test_data_movies.json'))
def test_create_movie_object(movie_resp: Dict[str, Any]):
    """ Tests API movie response to movie object transform"""
    movie_obj = client._from_resp_to_movie(movie_resp=movie_resp)
    assert movie_resp['Title'] == movie_obj.title
    assert movie_resp['imdbID'] == movie_obj.imdbid

@pytest.mark.parametrize('search_resp', read_test_data_from_json('test_data/test_data_search.json'))
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







# def test_url(requests_mock):
#     requests_mock.get('http://test.com', text='data')
#     assert 'data' == requests.get('http://test.com').text

# def test_get(requests_mock):
#     requests_mock.get('http://www.omdbapi.com/', text='data')
#     assert 'data' == omdb_get('http://www.omdbapi.com/?i=tt3896198&apikey=83c6dc42')

# def omdb_get(url: str) -> str:
#     return requests.get(url).text

