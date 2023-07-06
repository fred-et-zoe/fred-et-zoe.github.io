#!/usr/bin/python3

from datetime import datetime, timedelta, timezone

import frontmatter
import git
import os
import re
import sys

date_re = '[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}'
repo = git.Repo('.')

def publication_commit(file_name):
    for [commit, lines] in repo.blame(rev='HEAD', file=file_name):
        for l in lines:
            if re.fullmatch('draft: *false', l):
                return commit

def fixup_date(file_name):
    c = publication_commit(file_name)

    if c is None:
        return

    author_tz = timezone(timedelta(seconds=-c.author_tz_offset))
    author_datetime = datetime.fromtimestamp(c.authored_date, timezone.utc).astimezone(author_tz)

    post = frontmatter.load(file_name)
    old_date = post['date'].date()
    new_date = author_datetime.date()
    post['date'] = author_datetime

    jour = new_date.isoformat()

    old_cover = post['cover']
    new_cover = re.sub('^' + date_re, jour, old_cover)
    post['cover'] = new_cover

    with open(file_name, 'wb') as f:
        frontmatter.dump(post, f, sort_keys=False)
        f.write(b'\n')

    repo.index.add(file_name)

    if old_date != new_date:
        new_name = re.sub(date_re + r'(?=-[^/\\]*\.md$)', jour, file_name)
        repo.git.mv(file_name, new_name)

    if old_cover != new_cover:
        repo.git.mv(os.path.join('static', 'images', old_cover), os.path.join('static', 'images', new_cover))

for f in sys.argv[1::]:
    fixup_date(f)
