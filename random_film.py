#!/usr/bin/env python3

import argparse
import random
import webbrowser

import json_lines

"""
Example output:
{
   "title":"2 or 3 Things I Know About Her",
   "url":"https://www.criterionchannel.com/2-or-3-things-i-know-about-her",
   "img":"https://vhx.imgix.net/criterionchannelchartersu/assets/bff62486-e5e9-4e8d-ad75-436cb2cf12c9.jpg?auto=format%2Ccompress&fit=crop&h=140&q=100&w=250",
   "country":"France",
   "year":"1967"
}
"""


def main(filename) -> dict:
    count = 0
    selection = None
    with open(filename, 'rb') as f:
        for item in json_lines.reader(f):
            count += 1
            if random.randint(1, count) == count:
                selection = item
    return selection


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Find a random film from Criterion Channel'
    )
    parser.add_argument('-f', '--file',
                        help='Path to .jl file',
                        required=True)
    parser.add_argument('-b', '--browse',
                        help='Open in a browser',
                        dest='browse', action='store_true')
    args = parser.parse_args()

    if not args.file:
        parser.print_help()
        print("")
    else:
        film = main(args.file)
        print(f'Your selection is ')
        print(f'   Title: {film["title"]} ({film["year"]})')
        print(f'   Country: {film["country"]}')
        if args.browse:
            webbrowser.open_new_tab(film['url'])
