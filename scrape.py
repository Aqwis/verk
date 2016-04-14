#!/usr/bin/env python3

import sys
from bs4 import BeautifulSoup

filename = sys.argv[1]
f = open(filename)
html = f.read()

soup = BeautifulSoup(html, 'html.parser')
contents_list = soup.find_all("section", class_='article')

if len(contents_list) > 1:
    raise Exception()

contents = contents_list[0]
try:
    contents.find(class_='factboxcontainer').decompose()
except:
    pass
lines = list([s.replace('\n', ' ') for s in contents.stripped_strings])
print(" ".join(lines))