#!/usr/bin/python3

import datetime
import fileinput
import git
import os
import re
import sys

repo = git.Repo('.')
f = sys.argv[1]

def publication_commit(f):
    for [commit, lines] in repo.blame(rev='HEAD', file=f):
        for l in lines:
            if re.fullmatch('draft: *false', l):
                return commit

c = publication_commit(f)

if c is None:
    sys.exit(1)

author_tz = datetime.timezone(datetime.timedelta(seconds=-c.author_tz_offset))
author_date = datetime.datetime.fromtimestamp(c.authored_date, datetime.timezone.utc).astimezone(author_tz)

for l in fileinput.input(files=[f], inplace=True):
    if re.match('^date:', l):
        print(f"date: {author_date.isoformat()}")
    else:
        print(l,end='')

