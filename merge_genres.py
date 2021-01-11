#!/usr/bin/env python3

import argparse

import json_lines
import orjson


def main(filename) -> list:
    movies: dict = {}
    with open(filename, 'rb') as f:
        for movie in json_lines.reader(f):
            slug = movie['slug']
            existing_movie = movies.get(slug, None)
            if existing_movie:
                if 'genre' in movie:
                    existing_movie['genre'].append(movie['genre'])
            else:
                if 'genre' in movie and movie['genre']:
                    movie['genre'] = [movie['genre']]
                else:
                    movie['genre'] = []
                movies[movie['slug']] = movie
    return list(movies.values())


def as_jl(films: list) -> str:
    result = '[\n'
    for film in films:
        json_bytes = orjson.dumps(film)
        result = result + json_bytes.decode('utf-8') + '\n'
    result = result + ']'
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Take duplicate movies and merge string genres into an array'
    )
    parser.add_argument('-f', '--file',
                        help='Path to .jl file',
                        required=True)
    args = parser.parse_args()

    if not args.file:
        parser.print_help()
        print("")
    else:
        films = main(args.file)
        print(as_jl(films))
