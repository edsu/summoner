summoner
========

[![Build Status](https://secure.travis-ci.org/edsu/summoner.png)](http://travis-ci.org/edsu/summoner)

Work with the [Serial Solutions Summon API](http://api.summon.serialssolutions.com/) from Python.

```python
from summoner import Summon

summon = Summon(summon_id, summon_secret_key)
results = summon.search("Web")

for doc in results['documents']:
  print doc['Title']
```

You can pass in any of the optional parameters supported by the Summon API
by using the parameter name without the `s.` prefix. So for example to 
turn highlighting off:

```python
results = summon.search("Web", hl=False)
```

Or to facet by subject:

```python
results = s.search('World Wide Web', ff='SubjectTerms,or')
```

Develop
-------

To run the tests you'll need to set the `SUMMON_APP_ID` and `SUMMON_SECRET_KEY`
in your environment.

1. pip install -r requirements.txt
1. py.test test.py

