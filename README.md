# OMDbCLI
A simple CLI tool to run searches for movies and get details about movies from the OMDbAPI.

# Installation
TBD

# Usage

commands:
  {search,get}
    search      Get a list of movies matching the following critria
    get         Gets the details for the movie best matching the following critria

## Search
optional arguments:
  -h, --help     show this help message and exit
  --title TITLE  Limits the search to movies with this word in the title. IE: "star" will find Starwars movies (Used with: --search OR
                 --get)
  --year YEAR    Limits your search to a particular year. (Used with: --search OR --get)

## Get
optional arguments:
  -h, --help       show this help message and exit
  --title TITLE    Limits the search to movies with this word in the title. IE: "star" will find Starwars movies (Used with: --search OR
                   --get)
  --year YEAR      Limits your search to a particular year. (Used with: --search OR --get)
  --imdbid IMDBID  Will find the movie with this IMDB Id number (Used for: --get only)

# Disclaimer
This project is in no way endorsed or related to OMDBApi in any official capacity. It's just a tool I made.