# Scrapeterion

A very simple command-line interface for extracting and saving a list of
movies that are available at [Criterion Channel](https://films.criterionchannel.com/),
then selecting a random movie from the list.

(Tested only on linux.)

# Setup

Install python3 (preferably in a virtual environment), then

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
