import shodan

SHODAN_API_KEY = "ch0KPiOvr34Tf3It6N5EqhSjEgEuEb0F"

api = shodan.Shodan(SHODAN_API_KEY)

# Search Shodan
results = api.search('politiet.no')

# Show the results
print('Results found: {}'.format(results['total']))
for result in results['matches']:
        print('IP: {}'.format(result['ip_str']))
        print(result['data'])