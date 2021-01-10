# Scrapeterion

A very simple command-line interface for extracting and saving a list of
movies that are available at [Criterion Channel](https://films.criterionchannel.com/),
then selecting a random movie from the list.
 
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

Choose a random film from the list:

```bash
./random_film.py -f films.jl
```

Go to a random criterion movie page in your default browser:

```bash
./random_film.py -f films.jl -b
```

## Export Formats

Depending on the format, each film look
something like this:

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

You can also export as `json`, `csv`, or even `xml`
by changing the file extension:

```bash
# CSV
scrapy crawl films -O films.csv

# JSON
scrapy crawl films -O films.json

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

## Tycherion

This library is used to generate random
film suggestions at [Tycherion](https://mikebridge.github.io/tycherion/).
