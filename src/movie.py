""" Contains the dataclasses for this tool to help keep the code readable"""

from typing import Dict, List

from dataclasses import dataclass

@dataclass
class Movie:
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
    