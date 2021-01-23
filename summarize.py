#!/usr/bin/env python3

import argparse

import json_lines
# reading a file with keys:
# "title", "url", "img", "country", "year", "director"
import orjson


def main(filename) -> dict:
    count = 0
    directors = {}
    countries = {}
    years = {}
    with open(filename, 'rb') as f:
        item: dict
        #for item_raw in json_lines.reader(f):
        for item in orjson.loads(f.read()):
            # item = item_raw.rstrip(' ,')
            # if len(item) < 2:
            #     continue
            count = count + 1
            extract_director(directors, item)
            extract_item(years, 'year', item)
            extract_item(countries, 'country', item)
    return {
        'count': count,
        'directors': directors,
        'countries': countries,
        'years': years
    }


def extract_director(directors, item) -> dict:
    # directors is mutable
    if item['director']:
        name = item['director']
        directors[name] = directors.get(name, {
            'name': name,
            'count': 0
        })
        directors[name]['count'] = directors[name]['count'] + 1
    return directors


def extract_item(summary_dict: dict, key: str, item: dict) -> dict:
    # summary_dict is mutable
    if item[key]:
        v = item[key]
        summary_dict[v] = summary_dict.get(v, 0)
        summary_dict[v] = summary_dict[v] + 1
    return summary_dict


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Summarize output from scrapeterion'
    )
    parser.add_argument('-f', '--file',
                        help='Path to .jl file',
                        required=True)
    args = parser.parse_args()

    if not args.file:
        parser.print_help()
        print('')
    else:
        summary = main(args.file)
        json_bytes = orjson.dumps(
            summary, option=orjson.OPT_INDENT_2 | orjson.OPT_SORT_KEYS)
        print(json_bytes.decode('utf-8'))
