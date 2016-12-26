#!/usr/bin/env python

import csv
from datetime import datetime
from dateutil import parser

import click


def describe(_c):
    "this creates the data to be in a useful format"
    headers = _c.next()
    data = []
    for item in _c:
        _d = {}
        for idx, field in enumerate(headers):
            try:
                _d[field] = item[idx]
            except IndexError:
                print repr(item)
        data.append(_d)
    return data


def getdata(fn):
    "this takes a CSV file and returns a useful format"
    _csv = csv.reader(fn)
    return describe(_csv)


@click.command()
@click.argument('input', type=click.File('r'))
@click.option('--start', type=click.STRING, help='start date for filter')
@click.option('--end', type=click.STRING, help='end date for filter')
def harvestSelector(input, start=False, end=False):
    data = getdata(input)
    if start:
        _s = parser.parse(start)
        data = [x for x in data if _s <= parser.parse(x['Date'])]
                 
    if end:
        _e = parser.parse(end)
        data = [x for x in data if parser.parse(x['Date']) <= _e]

    print sum([float(x['Hours']) for x in data])

if __name__ == '__main__':
    harvestSelector()
