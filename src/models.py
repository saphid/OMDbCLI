""" Contains the data models for this tool to help keep the code readable"""

from typing import Dict, List, Optional

from dataclasses import dataclass

@dataclass
class Movie:
    """ Holds all the data for a movie """
    title: str
    year: str
    imdbid: str
    item_type: str
    poster: str

    rated: str = ""
    released: str = ""
    runtime: str = ""
    genre: str = ""
    director: str = ""
    writer: str = ""
    actors: str = ""
    plot: str = ""
    language: str = ""
    country: str = ""
    awards: str = ""
    ratings: List = None
    metascore: str = ""
    imdbrating: str = ""
    imdbvotes: str = ""
    dvd: str = ""
    boxoffice: str = ""
    production: str = ""
    website: str = ""
    response: str = ""

class Query():
    """ This class gives a userfriendly interface to create queries.
        Can return OMDBAPI params
    """
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
