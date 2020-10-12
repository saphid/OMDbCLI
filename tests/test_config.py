""" This teasts the config manager"""

import os

from typing import Dict

import pytest

from src.config import ConfigManager
from test_data.test_objects import TestData


@pytest.mark.parametrize('api_key', TestData.configs())
def test_load_update_config(api_key: str, mocker):
    """ Tests loading config from mocked config file

    Args:
        api_key (str): To be mocked into _load_config
    """
    mocker.patch('src.config.ConfigManager._load_config',
                 return_value={'api_key': api_key})
    config = ConfigManager()
    assert config.api_key == api_key


@pytest.mark.parametrize('api_key', TestData.configs())
def test_invalidate_key(api_key: str, mocker):
    """ Tests invalidating stored api keys

    Args:
        api_key (str): To be mocked into _load_config
    """
    mocker.patch('src.config.ConfigManager._load_config',
                 return_value={'api_key': api_key})
    mocker.patch('src.config.ConfigManager.prompt_for_key',
                 return_value={
                     'api_key': 'replacement',
                     'old_api_key': api_key
                 })
    config = ConfigManager()
    assert config.api_key == api_key
    config.invalidate_key()
    assert config.old_api_key == api_key
    assert config.api_key == 'replacement'
