#!/usr/bin/python3

import argparse

parser = argparse.ArgumentParser()

parser.add_argument('filename', help = 'The file with some extension')

args = parser.parse_args()

try:
    fname = args.filename
    extension = fname.split('.')[1]
    print(f"Extension of file is: {extension}")
except IndexError as ie:
    print(f"Error: {ie}, you didn't pass the file with extension")

