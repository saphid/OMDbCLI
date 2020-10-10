""" This module is to hold the query class.

    The query object is a clean way to make a query and return parameters for OMDBAPI
"""

from typing import Dict, Optional

class Query():
    """ This class gives a userfriendly interface to create queries. Can return OMDBAPI params """

    def __init__(self,
                 search: str = None,
                 title: str = None,
                 imdbid: str = None,
                 year: str = None,
                 plot: str = None,
                 item_type: str = None,
                 page: str = "1"):
        self.search = search
        self.title = title
        self.imdbid = imdbid
        self.year = year
        self.plot = plot
        self.item_type = item_type
        self.page = page

    @property
    def params(self) -> Dict[str, Optional[str]]:
        """ Returns OMDbAPI Friendly parameters"""
        params = {
        's': self.search,
        't': self.title,
        'i': self.imdbid,
        'y': self.year,
        'page': self.page,
        'plot': self.plot,
        'type': self.item_type
        }
        params = {k:v for k,v in params.items() if v is not None}
        return params
