#!/usr/bin/env python3

import argparse
import random

import json_lines

"""
{
   "title":"2 or 3 Things I Know About Her",
   "url":"https://www.criterionchannel.com/2-or-3-things-i-know-about-her",
   "img":"https://vhx.imgix.net/criterionchannelchartersu/assets/bff62486-e5e9-4e8d-ad75-436cb2cf12c9.jpg?auto=format%2Ccompress&fit=crop&h=140&q=100&w=250",
   "country":"France",
   "year":"1967"
}
"""

def main(filename):
    count = 0
    selection = None
    with open(filename, 'rb') as f:
        for item in json_lines.reader(f):
            count += 1
            if random.randint(1, count) == count:
                selection = item
    print(f'Your selection is ')
    print(f'   Title: {selection["title"]} ({selection["year"]})')
    print(f'   Country: {selection["country"]}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Find a random film from Criterion Channel'
    )
    parser.add_argument('-f', '--file',
                        help='Path to .jl file',
                        required=True)
    args = parser.parse_args()

    if not args.file:
        parser.print_help()
        print("")
    else:
        # print('File is {}'.format(args.file))
        main(args.file)
