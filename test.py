import os
import pytest

from summoner import Summon

"""
You'll need to set SUMMON_APP_ID and SUMMON_SECRET_KEY in your environment if 
you want to run these tests.
"""

app_id = os.environ['SUMMON_APP_ID']
secret_key = os.environ['SUMMON_SECRET_KEY']

def test_status():
    s = Summon(app_id, secret_key)
    assert s.status() == 'available'

def test_search():
    s = Summon(app_id, secret_key)
    results = s.search('The Bluest Eye')
    assert len(results['documents']) > 0

def test_facet():
    s = Summon(app_id, secret_key)
    results = s.search('World Wide Web', ff='SubjectTerms,or')
    assert len(results['documents']) > 1
    assert len(results['facetFields']) == 1

def test_multiple_facets():
    s = Summon(app_id, secret_key)
    results = s.search('World Wide Web', ff=['SubjectTerms,or', 'ContentType,or'])
    assert len(results['documents']) > 1
    assert len(results['facetFields']) == 2

def test_highlighting():
    s = Summon(app_id, secret_key)
    results = s.search('World Wide Web', hl=False)
    for doc in results['documents']:
        assert '<h>' not in doc['Title']

def test_unicode():
    s = Summon(app_id, secret_key)
    results = s.search(u'\u6751\u4e0a\u6625\u6a39')
    assert len(results['documents']) > 1

def test_access_id_none():
    with pytest.raises(Exception) as e:
        s = Summon(None, '123')
    assert e.exconly() == 'Exception: access_id must not be None'

def test_secret_key_none():
    with pytest.raises(Exception) as e:
        s = Summon('123', None)
    assert e.exconly() == 'Exception: secret_key must not be None'
