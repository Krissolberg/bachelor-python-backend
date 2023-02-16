import shodan

SHODAN_API_KEY = "HfDcFJOFVgov1yFgDuDPVe3ExvNbYViP"

api = shodan.Shodan(SHODAN_API_KEY)


def shodanSearch(input):
    # Search Shodan
    data, ip, org = [], [], []
    results = api.search(input)

    # Show the results
    for result in results['matches']:
        ip.append(result['ip_str'])
        org.append(result['org'])

    for j in [input, results['total'], ip, org]:
        data.append(j)
    return data


def shodanHost(ips):
    global port, versions, cipher

    host = api.host(ips)

    data3 = {host['ip_str']: {}}

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
        data3[key] = value

    # print(json.dumps(data3, indent=6))

    return data3
