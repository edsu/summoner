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
