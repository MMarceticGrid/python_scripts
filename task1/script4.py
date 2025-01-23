#!/usr/bin/python3

import argparse
from collections import Counter

parse = argparse.ArgumentParser()

parse.add_argument('string', help = "Input string")

args = parse.parse_args()

input_string = args.string

char_count = Counter(input_string)

print(f"{input_string}")
for char, count in char_count.items():
    print(f"{char}:{count}")


