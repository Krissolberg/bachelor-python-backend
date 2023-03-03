import ipaddress
import json
import shodan

import apiExtentions.shodanDataFilter as shodanFilter

auth = "YzZmjxnuVu8cr0H5HCpMcjFrLMG1zVFP"


def shodanSearch(indata):
    # Search Shodan
    ip, org = [], []
    data = {indata: {}}

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

    datatemp = {indata: {'result': results['total'],
                         'ip': ip,
                         'org': org}}

    for key, value in datatemp.items():
        data[key] = value

    return data


def shodanHost(ips):
    global port, versions, cipher

    host = shodan.Shodan(auth).host(ips)

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
            vulns = shodanFilter.getVulns(host['data'])
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

    data3 = {host['ip_str']: {}}
    for key, value in data.items():
        data3[key] = value

    # print(json.dumps(data3, indent=6))

    return data3


def sok(inndata):
    # inndata er et array, denne kan inneholde både URL og IP

    # Filtrer ut IP-ene fra inndata
    iprange, iprangesplit, ip = shodanFilter.filterUrlIp(inndata)

    # Filtrerer ut funnet IP av inndata
    url = list(set(inndata) - set(iprange) - set(ip))

    # Lager individuell ip for range, og legger det i ip-array
    for i in iprangesplit:
        intRange = ((int(ipaddress.ip_address(i[1]))) - int(ipaddress.ip_address(i[0])))
        for j in range(intRange):
            ip.append(str(ipaddress.ip_address(int(ipaddress.ip_address(i[0])) + j)))

    # Gjør en shodanSearch på Url, og legger funnet IP til ips-variabelen
    searchresult = []
    for i in url:
        temp = shodanSearch(i)
        searchresult.append(temp)
        ip.extend(temp[i]['ip'])

    # Gjør en fullstendig søk på hver IP og skriver ut ønsket data
    hostresult = []
    if len(ip) > 0:
        for i in ip:
            try:
                hostresult.append(shodanHost(i))
            except:
                hostresult.append({i: 'No result'})

    # print(json.dumps(hostresult, indent=6))

    result = [searchresult, hostresult]
    return result


# print(json.dumps(data3, indent=6))

print(json.dumps(sok(["163.174.115.35-163.174.115.45"]), indent=6))
