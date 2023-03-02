import json
import shodan

auth = "YzZmjxnuVu8cr0H5HCpMcjFrLMG1zVFP"


def shodanSearch(indata):
    # Search Shodan
    ip, org = [], []
    data3 = {indata: {}}

    results = shodan.Shodan(auth).search(indata)

    # Show the results
    for result in results['matches']:
        try:
            ip.append(result['ip_str'])
        except:
            break
        try:
            org.append(result['org'])
        except:
            break

    datad = {indata: {'result': results['total'],
                      'ip': ip,
                      'org': org}}

    for key, value in datad.items():
        data3[key] = value

    return data3


def getVulns(data):
    vulns = []

    for item in data:
        for i in item:
            if i == 'vulns':
                if len(vulns) == 0:
                    vulns.append(item[i])
                else:
                    if item[i] not in vulns:
                        vulns.append(item[i])

    return vulns[0]


def shodanHost(ips):
    global port, versions, cipher

    host = shodan.Shodan(auth).host(ips)

    data3 = {host['ip_str']: {}}

    for item in host['data']:
        port = item['port']
        try:
            versions = item['ssl']['versions']
        except:
            versions = "Not found"
        try:
            cipher = item['ssl']['cipher']
        except:
            cipher = "Not found"
        try:
            vulns = getVulns(host['data'])
        except:
            vulns = "Not found"

    data = {host['ip_str']: {'org': host['org'],
                             'os': host['os'],
                             'hostnames': host['hostnames'],
                             'domains': host['domains'],
                             'port': port,
                             'versions': versions,
                             'cipher': cipher,
                             'vulns': vulns}}

    for key, value in data.items():
        data3[key] = value

    # print(json.dumps(data3, indent=6))

    return data3
