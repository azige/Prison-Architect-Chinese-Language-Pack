#!/usr/bin/python3 

import os
import re

BASE_PATH = os.path.dirname(__file__)
BASE_DATA_PATH = os.path.join(BASE_PATH, "../data/language")

trans = dict()

def should_skip(line):
    striped = line.strip()
    return striped.startswith("#") or len(striped) <= 1


def update_file(base_file, origin_file, out_file):
    with open(base_file) as inf:
        for line in inf:
            if should_skip(line):
                continue

            index = line.find(" ")
            if index == -1:
                # not translation string
                continue

            key = line[:index]
            value = line[index + 1:]
            trans[key] = value.strip()

    print("translated string size: %d" % len(trans))

    line_num = 0
    with open(origin_file) as base:
        with open(out_file, "w+") as output:
            regex = re.compile("(\w+)(\s+)(.+)$")

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

for name in ['base-language', 'fullgame', 'tablets']:
    print("processing %s" % name)
    base_file = os.path.join(BASE_DATA_PATH, name + '.txt')
    origin_file = os.path.join(BASE_DATA_PATH, name + '-origin.txt')
    out_file = base_file

    update_file(base_file, origin_file, out_file)
