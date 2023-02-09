import requests_cache
from requests_cache import CachedSession
from datetime import timedelta

requests_cache.install_cache('shodan_cache')

session = CachedSession(
    'shodan_cache',
    use_cache_dir=True,
    cache_control=True,
    expire_after=timedelta(days=1),
    allowable_methods=['GET'],
    allowable_codes=[200],
    match_headers=True
)