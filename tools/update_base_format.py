#!/usr/bin/python3 

import re

BASE_FILE_NAME = "base-language.txt"
ORIGIN_FILE_NAME = "base-language-alpha34.txt"
OUTPUT_FILE_NAME = "output.txt"

trans = dict()

def should_skip(line):
    return line.startswith("#") or line.startswith(" ") or len(line) <= 1


with open(BASE_FILE_NAME) as inf:
    for line in inf:
        if should_skip(line):
            continue

        index = line.find(" ")
        if index == -1:
            # not translation string
            continue

        key = line[:index]
        value = line[index + 1:]
        trans[key] = value

print("translated string size: %d" % len(trans))

with open(ORIGIN_FILE_NAME) as base:
    with open(OUTPUT_FILE_NAME, "w+") as output:
        regex = re.compile("(\w+)(\s+)(.+)")

        for line in base:
            if should_skip(line):
                output.write(line)
                continue

            match = regex.match(line)
            assert match is not None, "match failed, %s" % line

            key = match.group(1)
            space = match.group(2)
            value = trans[key]
            if value is None:
                print("Missing translation: %s" % key)
                value = "[TODO]" + match.group(3)
            else:
                value += "\n"

            output.write("%s%s%s" % (key, space, trans[key]))

