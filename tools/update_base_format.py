#!/usr/bin/python3 

import os
import re

BASE_PATH = os.path.dirname(__file__)
BASE_DATA_PATH = os.path.join(BASE_PATH, "../data/language")

trans = dict()
regex = re.compile("(\w+)([\s\t]+)(.+)$")

def should_skip(line):
    striped = line.strip()
    return striped.startswith("#") or len(striped) <= 1

def read_base_file(base_file):
    with open(base_file) as inf:
        for line in inf:
            if should_skip(line):
                continue

            match = regex.match(line)
            if match is None:
                # not translation string
                continue

            key = match.group(1)
            value = match.group(3)
            if value.startswith('[TODO]'):
                # not translate yet
                continue

            trans[key] = value.strip()

def update_base_file(origin_file, out_file):
    line_num = 0

    with open(origin_file) as base:
        with open(out_file, "w+") as output:

            for line in base:
                line_num += 1
                if should_skip(line):
                    output.write(line)
                    continue

                match = regex.match(line)
                assert match is not None, "match failed, '%s':%d" % (line, line_num)

                key = match.group(1)
                space = match.group(2)
                value = trans.get(key)
                if value is None:
                    print("Missing translation: %s" % key)
                    value = "[TODO]" + match.group(3)

                output.write("%s%s%s\n" % (key, space, value))

file_names = ['base-language', 'fullgame', 'tablets']

for name in file_names:
    base_file = os.path.join(BASE_DATA_PATH, name + '.txt')
    read_base_file(base_file)

for name in file_names:
    origin_file = os.path.join(BASE_DATA_PATH, name + '-origin.txt')
    out_file = os.path.join(BASE_DATA_PATH, name + '.txt')
    update_base_file(origin_file, out_file)
