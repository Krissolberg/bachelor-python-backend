import requests
import requests_cache

requests_cache.install_cache('demo_cache')
requests.get('http://httpbin.org/delay/1')