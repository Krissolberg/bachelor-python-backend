import json

from collections import defaultdict

import shodan
import sys
import os
import cacheService

SHODAN_API_KEY = ""

api = shodan.Shodan(SHODAN_API_KEY)


def shodanSearch(input):
    # Search Shodan
    results = api.search(input)
    data = []

    # Show the results
    print('Results found: {}'.format(results['total']))
    for result in results['matches']:
        data.append([result['ip_str'], result['org']])
    return data


def shodanHost(ips):
    # Lookup the host
    data3 = defaultdict(list)
    for i in ips:
        host = api.host(i)

        for item in host['data']:
            port = item['port']
            try:
                versions = item['ssl']['versions']
                cipher = item['ssl']['cipher']
            except:
                versions = "tom"

        data = {host['ip_str']: {'org': host['org'],
                                 'os': host['os'],
                                 'domains': host['domains'],
                                 'port': port,
                                 'versions': versions,
                                 'cipher': cipher}}
        for key, value in data.items():
            data3[key].append(value)

    print(json.dumps(data3, indent=6))
