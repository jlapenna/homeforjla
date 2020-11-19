#!/usr/bin/env python3

import csv
import io
import urllib.parse

from bs4 import BeautifulSoup

def main():
    soup = BeautifulSoup(open('examples/saved.html'), 'lxml')
    rows = []
    for tag in soup.select('.searchResult'):
        num = select_str(tag, '.listingNum').split(' ')[1]
        rows.append({
            'address': select_str(tag, '.address span'),
            'price': select_str(tag, '.rapIDXSearchResultsPriceTop'),
            'dom': select_str(tag, '.listingDomCdom .display-label'),
            'sqft': select_str(tag, '.listingSqFt .display-label'),
            'beds': select_str(tag, '.listingBeds .display-label'),
            'baths': str(select_str(tag, '.listingBaths .display-label')),
            'num': num,
            'url': 'https://www.google.com/search?q=%s&btnI' % urllib.parse.quote('redfin' + num),
            'remarks': select_str(tag, '.remarks-long'),
        })
    
    s = io.StringIO()
    c = csv.DictWriter(s, ('address', 'price', 'dom', 'sqft', 'beds', 'baths', 'num', 'url', 'remarks', 'visited', 'notes'))
    c.writeheader()
    c.writerows(rows)
    s.seek(0)
    print(s.read())
    s.close()


def select_list(soup, query):
    return [tag.get_text(' ', strip=True) for tag in soup.select(query)]


def select_str(soup, query):
    return ' '.join(select_list(soup, query))

if __name__ == '__main__':
    main()
