#!/usr/bin/python3

import argparse

parser = argparse.ArgumentParser()

parser.add_argument('filename', help='Filename of log file')

args = parser.parse_args()
logfile = args.filename

agents = {}

with open(logfile, 'r') as f:
    for line in f:
        UserAgent = line.split('"')[-2]
        if UserAgent in agents.keys(): 
            agents[UserAgent] += 1
        else:
            agents[UserAgent] = 1


for agent in agents:
    print(f"{agent}")
