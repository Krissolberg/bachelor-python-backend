import shodan
import sys
import os

from dotenv import load_dotenv

load_dotenv() # take environment from .env.


SHODAN_API_KEY = os.getenv("API_KEY")

api = shodan.Shodan(SHODAN_API_KEY)

input = sys.argv[0]

def shodanSearch(input):
    # Search Shodan
    results = api.search('input')

    # Show the results
    print('Results found: {}'.format(results['total']))
    for result in results['matches']:
            print('IP: {}'.format(result['ip_str']))
            print(result['data'])

# Lookup the host
host = api.host('163.174.115.13')

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

