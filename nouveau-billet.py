#!/usr/bin/python3

from datetime import date, datetime, time, timedelta, timezone
from unidecode import unidecode

import frontmatter
import os
import re
import sys

titre = ' '.join(sys.argv[1::]).capitalize()
chapo = re.sub('[^a-z]+', '-', unidecode(titre).lower())
tz = datetime.now(timezone.utc).astimezone().tzinfo
draft = True

jour = None
heure = os.environ.get('DATETIME')
if heure:
    heure = datetime.fromisoformat(heure)
    if not heure.tzinfo:
        heure = heure.replace(tzinfo=tz)
else:
    jour = os.environ.get('DATE')
    if jour:
        jour = date.fromisoformat(jour)
        heure = datetime.combine(jour, time(hour=9, tzinfo=tz))

if not heure:
    heure = datetime.now(tz).replace(microsecond=0) + timedelta(minutes=15)
    draft = False

if not jour:
    jour = heure.date()

jour = jour.isoformat()

post = frontmatter.loads("")
post['title'] = titre
post['date'] = heure
post['draft'] = draft
post['cover'] = f'{jour}-{chapo}.jpg'

with open(f'content/billets/{jour}-{chapo}.md', 'wb') as f:
    frontmatter.dump(post, f, sort_keys=False)

with open(f'static/images/{jour}-{chapo}.jpg', 'w'):
    pass
