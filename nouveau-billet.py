#!/usr/bin/python3

from unidecode import unidecode

import datetime
import os
import re
import sys

titre = ' '.join(sys.argv[1::]).capitalize()
chapo = re.sub('[^a-z]+', '-', unidecode(titre).lower())
tz = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo

jour = None
heure = os.environ.get('DATETIME')
if heure:
    heure = datetime.datetime.fromisoformat(heure)
    if not heure.tzinfo:
        heure = heure.replace(tzinfo=tz)
else:
    jour = os.environ.get('DATE')
    if jour:
        jour = datetime.date.fromisoformat(jour)
        heure = datetime.datetime.combine(jour, datetime.time(hour=9, tzinfo=tz))

if not heure:
    heure = datetime.datetime.now(tz).replace(microsecond=0)

if not jour:
    jour = heure.date()

heure = heure.isoformat()
jour = jour.isoformat()

content=f'''\
---
title: {titre}
date: {heure}
draft: true
cover: {jour}-{chapo}.jpg
---
'''

with open(f'content/billets/{jour}-{chapo}.md', 'w') as f:
    f.write(content)

with open(f'static/images/{jour}-{chapo}.jpg', 'w'):
    pass
