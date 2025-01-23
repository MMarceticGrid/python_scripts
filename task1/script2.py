#!/usr/bin/python3

import argparse

parser = argparse.ArgumentParser()

parser.add_argument('numbers', help = 'List of integers', type = int, nargs = '+')

args = parser.parse_args()

set_of_numbers = set(args.numbers)

num_tuple = tuple(set_of_numbers)

max_value = max(num_tuple)
min_value = min(num_tuple)

print(f"{num_tuple}, Max value: {max_value}, Min value: {min_value}")