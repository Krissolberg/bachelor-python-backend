from requests_cache import CachedSession, install_cache
from datetime import timedelta

install_cache(
    'shodan_cache',
    backend="mongodb"
    )

session = CachedSession(
    'shodan_cache',
    backend='mongodb',
    use_cache_dir=True,
    cache_control=True,
    expire_after=timedelta(days=14),
    allowable_methods=['GET'],
    allowable_codes=[200, 404],
    match_headers=True
)

nosession = CachedSession(
    'shodan_cache',
    backend='mongodb',
    use_cache_dir=False,
    cache_control=True,
)