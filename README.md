summoner
========

[![Build Status](https://secure.travis-ci.org/edsu/summoner.png)](http://travis-ci.org/edsu/summoner)

Work with the [Serial Solutions Summon API](http://api.summon.serialssolutions.com/) from Python.

```python

from summoner import Summon

s = Summon(summon_id, summon_secret_key)

for doc in s.search("World Wide Web"):
  print doc.title

```

Develop
-------

To run the tests you'll need to set the `SUMMON_APP_ID` and `SUMMON_SECRET_KEY`
in your environment.
