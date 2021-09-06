# Scrapeterion

A very simple command-line interface for extracting and saving a list of
movies that are available at [Criterion Channel](https://films.criterionchannel.com/).
 
# Setup

- Install [python3](https://www.python.org/download/releases/3.0/)
- Install a virtual environment (optional)

```bash
# Linux
python3 -m venv scrapeterion
. ./scrapeterion/bin/activate
```

Install the libraries via pip:

```bash
python -m pip install -r requirements.txt
```

# Usage

Save the list of films in `jl` format:

```bash
scrapy crawl films -O films.jl
```

By default this will return films available in the US only.  If you want films available in Canada (only), you can
add the two-letter ISO code `-a geo=CA`:

```bash
scrapy crawl films -a geo=CA -O films.jl
```

Choose a random film from the list:

```bash
./random_film.py -f films.jl
```

Go to a random criterion movie page in your default browser:

```bash
./random_film.py -f films.jl -b
```

## Export Formats

Depending on the format, each film looks something like this:

```json
{
  "title": "Belle de jour", 
  "url": "https://www.criterionchannel.com/belle-de-jour", 
  "img": "https://vhx.imgix.net/criterionchannelchartersu/assets/46bfd0a2-4448-4896-9b0f-cc755e212eb5.jpg", 
  "country": "France", 
  "year": "1967", 
  "director": "Luis Buñuel", 
  "slug": "belle-de-jour"
}
```

You can also export as `json`, `csv`, `jl` or even `xml`
by changing the file extension:

```bash
# CSV
scrapy crawl films -O films.csv

# JSON
scrapy crawl films -O films.json

# JL
scrapy crawl films -O films.jl

# XML
scrapy crawl films -O films.xml
```

## Genres

There is a separate script to extract the 
genre and director summaries.  At some point I'll
merge this separate script into the main "films" 
parser so that the resulting movies are categrorized. 

```
scrapy crawl genres -O genres.json
```

## Films By Genre

```
# for US only:
scrapy crawl films_by_genre -O genres.json

# or for Canada only:
scrapy crawl films_by_genre -a geo=CA -O genres.json
```

Note that this will return a film multiple times per genre.  You can merge
the genres as JL (and the geo code) with the merge_genres.py script.  This 
is probably the most complete data source, as each film will have a list
of genres and geo regions.  This script generates the most complete set of
data:

```bash
# get the movies available in the US
scrapy crawl films_by_genre -O genres_raw_us.jl

# get the movies available in Canada
scrapy crawl films_by_genre -a geo=CA -O genres_raw_ca.jl

# concatenate the files together
cat genres_raw_us.jl genres_raw_ca.jl genres_raw.jl

# merge the genres and geo locations
./merge_genres.py -f genres_raw.jl > genres.jl

# convert into JSON (using the [jq](https://stedolan.github.io/jq/) library)
cat tmp/genres_final.jl  | jq > tmp/genres_final.json
```

This generates a file with an array of json objects that look like this:

```json
{
  "title": "Across 110th Street",
  "url": "https://www.criterionchannel.com/across-110th-street",
  "img": "https://vhx.imgix.net/criterionchannelchartersu/assets/bd588e21-2211-4e36-b447-1a3947e24cf5.jpg",
  "country": "United States",
  "year": "1972",
  "director": "Barry Shear",
  "slug": "across-110th-street",
  "genre": [
    "action-adventure",
    "crime"
  ],
  "geo": [
    "CA",
    "US"
  ]
}
```

## Tycherion

This library is used to generate random
film suggestions at [Tycherion](https://mikebridge.github.io/tycherion/).
