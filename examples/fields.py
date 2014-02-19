#!/usr/bin/env python

"""
This script runs an open ended search of the Summon API and tallies up metadata 
fields used by content type. Adjust QUERY and PAGE_LIMIT as needed. You will
need to have your SUMMON_APP_ID and SUMMON_SECRET_KEY set in your 
environment.
"""

QUERY = "Web"
PAGE_LIMIT = 1000

import os
import sys
import time
from summoner import Summon

app_id = os.environ['SUMMON_APP_ID']
secret_key = os.environ['SUMMON_SECRET_KEY']
summon = Summon(app_id, secret_key)

stats = {}
recs = {}
total = 0
page = 0
errors = 0

while True:
    page += 1
    try:
        results = summon.search(QUERY, pg=page, ps=50)
    except Exception as e:
        errors += 1
        continue
    for doc in results['documents']:
        if len(doc['ContentType']) > 1:
            raise Exception("more than one ContentType: %s" % doc)

        content_type = doc['ContentType'][0]

        if not stats.has_key(content_type):
            stats[content_type] = {}
        if not recs.has_key(content_type):
            recs[content_type] = 0

        recs[content_type] += 1

        total += 1
        seen = {}
        for key in doc.keys():
            if not seen.has_key(key):
                stats[content_type][key] = stats[content_type].get(key, 0) + 1
            seen[key] = True

    if page >= PAGE_LIMIT:
        break

    sys.stderr.write("%s\n" % page)
    time.sleep(1)

def percentage(n, m):
    return "%02.1f%%" % (n / float(m) * 100)

print "records examined: %s" % total
print "errors: %s" % errors
content_types = stats.keys()

for ct in content_types:
    keys = stats[ct].keys()
    keys.sort(lambda b, a: cmp(stats[ct][a], stats[ct][b]))

    print
    print "<h3>%s (%s)</h3>" % (ct, percentage(recs[ct], total))

    print "<table>"
    for key in keys:
        print "<tr><td>%s</td><td>%s</td></tr>" % (key, percentage(stats[ct][key], recs[ct]))
    print "</table>"

