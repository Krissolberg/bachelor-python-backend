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


def shodanHost(input):
    # Lookup the host
    host = api.host(input)
    print(host)
    # Print general info
    print("""
IP: {}
Organization: {}
Operating System: {}
""".format(host['ip_str'], host.get('org', 'n/a'), host.get('os', 'n/a')))

    # Print all banners
    for item in host['data']:
        print("""
Port: {}
Banner: {}
""".format(item['port'], item['data']))
