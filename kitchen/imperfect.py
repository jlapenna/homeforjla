#!/usr/bin/env python3

import csv
import io
import re
import sys
import uuid
import pprint

from typing import List

HEADERS = ('Item', 'Category', 'Size', 'Quantity','Description', 'Staple', 'Last Modified', 'Key')

# RegEx that apply to the file loaded.
ALL_YOU_WERE_NOT_CHARGED = re.compile(
        r'\n(You were not charged for \d+ of this item.)\n');

# RegEx that apply to an individual line item.
FOOD_QUANTITY_PATTERN = re.compile(r'\ \((?P<Quantity>.*)\)', re.VERBOSE);
FOOD_TO_STRIP = [
        re.compile(r'^Conventional '),
        re.compile(r'^Imperfect Foods - '),
        re.compile(r'Organic '),
        ]
FOOD_FIELDS = re.compile(
        r'(?P<Item>.*) \((?P<Size>.*)\)\t(?P<Quantity>.*)\t(?P<Price>.*)$')
FOOD_PRIORITIES = [
        r'Grapes',
        r'Bacon',
        r'Potatoes',
        r'Eggs',
        r'Ribeye',
        r'Ground\ Beef',
        r'Chicken\ Broth',
        r'Ground\ Beef',
        ]
FOOD_PRIORITIES_PATTERN = re.compile(r'(?P<therest>.*)\ (?P<priority>(%s))' % '|'.join(FOOD_PRIORITIES), re.VERBOSE);


def load_items(order: List[str]):
    items = []
    for line in order.split('\n'):
        # V0 # line = FOOD_QUANTITY_PATTERN.sub('\t\g<Quantity>', line)
        for strip in FOOD_TO_STRIP:
            line = strip.sub('', line)
        # Re-order the words in an item's description to prioritze more
        # important terms
        line = FOOD_PRIORITIES_PATTERN.sub('\g<priority> \g<therest>', line)
        # V0 # line = line.split('\t')
        if not line:
            continue
        match = FOOD_FIELDS.match(line)
        if not match:
            sys.stdout.write('Could not match on %s', line)
        item = match.groupdict()
        # Strip columns we don't track
        del(item['Price'])
        # Add a unique Key
        item['Key'] = str(uuid.uuid4().hex)
        items.append(item)
    return items

def main():
    order = sys.stdin.read()
    order = ALL_YOU_WERE_NOT_CHARGED.sub('\t', order);
    items = load_items(order)

    s = io.StringIO()
    c = csv.DictWriter(s, HEADERS)
    c.writeheader()
    c.writerows(items)
    s.seek(0)
    print(s.read())
    s.close()


if __name__ == '__main__':
    main()
