import requests_cache
from requests_cache import CachedSession, MongoCache
from datetime import timedelta

requests_cache.install_cache('shodan_cache', backend="mongodb")
MongoCache(db_name='shodan_cache')


session = CachedSession(
    'shodan_cache',
    backend='mongodb',
    use_cache_dir=True,
    cache_control=True,
    expire_after=timedelta(days=1),
    allowable_methods=['GET'],
    allowable_codes=[200, 404],
    match_headers=True
)