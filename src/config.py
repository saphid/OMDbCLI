"""This module handles creating, loading, and updating the config file"""

import logging
import json
from typing import Dict

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class ConfigManager():
    """ This class creating, loading, and updating the config file,
        Also used to get and update the values of the config
    """

    def __init__(self):
        self._api_key = None
        self.old_api_key = None
        self._update_config(self._load_config())
        logging.debug('Loaded config: %s', vars(self))
        if not self._api_key:
            self._api_key = self.prompt_for_key().get('api_key')


    def invalidate_key(self):
        """ Wipes the current api key"""
        data = self.prompt_for_key()
        self._update_config_file(data)
        self._update_config(data=data)

    @property
    def api_key(self):
        """ Standard api_key property"""
        return self._api_key

    @api_key.setter
    def api_key(self, value):
        """ Stores the old value, then updates the variable and the config file """
        if self.api_key:
            self.old_api_key = self.api_key
        self._api_key = value
        self._update_config_file

    def save_config(self):
        """ Saves the current config to file"""
        self._update_config_file(data=data)

    def prompt_for_key(self) -> Dict:
        """ Prompt's the user to enter their API key"""
        api_key = input('Please enter your api key: ')
        logging.debug('prompt api_key %s', api_key)
        data = {'api_key': api_key} if api_key else self.prompt_for_key()
        logging.debug('prompt data: %s', data)
        return data

    def _update_config_file(self, data: Dict) -> None:
        """ Updates the config file with the current state this class"""
        with open('.conf','w') as conf_file:
            json.dump(data, conf_file)
    
    def _load_config(self):
        """ Loads the current config file"""
        try:
            with open('.conf', 'r') as conf_file:
                data = json.load(conf_file)
            if not data.get('api_key'):
                data = self.prompt_for_key()
                self._update_config_file(data)
        except (FileNotFoundError, json.decoder.JSONDecodeError) as err:
            logging.debug('load config: %s', err)
            data = self.prompt_for_key()
            self._update_config_file(data)
        return data
        
    def _update_config(self, data: Dict) -> None:
        """ Updates the class variables with data from data"""
        self._api_key = data.get('api_key', self._api_key)
        self.old_api_key = data.get('old_api_key', self.old_api_key)
