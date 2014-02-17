import os

from summoner import Summon

app_id = os.environ['SUMMON_APP_ID']
secret_key = os.environ['SUMMON_SECRET_KEY']

def test_status():
    s = Summon(app_id, secret_key)
    assert s.status() == 'available'

def test_search():
    s = Summon(app_id, secret_key)
    results = s.search('The Bluest Eye')
    assert len(results['documents']) > 0

def test_highlighting():
    s = Summon(app_id, secret_key)
    results = s.search('World Wide Web', hl=False)
    for doc in results['documents']:
        print doc['Title']

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

