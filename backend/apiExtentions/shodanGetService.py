import re

import shodan
import backend.apiExtentions.shodanDataFilter as shodanFilter
from backend import cacheService

auth = "wqBocETm9zujq2lWjSaYFUOFBhXDqeHV"


def shodanSearch(indata):
    ip, org = [], []
    limit = 200
    counter = 0
    results = []

    for banner in shodan.Shodan(auth).search_cursor(indata):

        results.append(banner)
        counter += 1
        if counter >= limit:
            break

    for result in results:
        try:
            ip.append(result['ip_str'])
        except:
            break
        try:
            org.append(result['org'])
        except:
            break

    data = {indata: {
        'ip': ip,
        'org': org}}

    return data


def shodanHost(ips):
    global port, versions, cipher, host
    try:
        host = (cacheService.session.get(
            f'https://api.shodan.io/shodan/host/{ips}?key={auth}').json())
        host['data']
        for item in host['data']:
            port = item['port']
            try:
                versions = []
                temp = item['ssl']['versions']
                for i in temp:
                    versions.append(re.sub(r'-', '', i, count=1))
            except:
                versions = "Not found"
            try:
                cipher = item['ssl']['cipher']
            except:
                cipher = "Not found"
            try:
                vulns = item['opts']['vulns']
            except:
                vulns = "Not found"

        data = {host['ip_str']: {'org': host['org'],
                                 'os': host['os'],
                                 'hostnames': host['hostnames'],
                                 'domains': host['domains'],
                                 'ports': host['ports'],
                                 'versions': versions,
                                 'cipher': cipher,
                                 'vulns': vulns}}

        return data
    except:
        raise SystemError("noresult")


def shodanDNS(domain):
    try:
        data = shodan.Shodan(auth).dns.domain_info(domain=domain, history=False, type=None, page=1)
        return data
    except:
        raise SystemError("Fant ingen DNS, fungerer API-key?")


def verifyKey():
    try:
        return cacheService.nosession.get(f'https://api.shodan.io/api-info?key={auth}', timeout=3,
                                          headers={'Cache-Control': 'no-cache, no-store'}).json()
    except:
        return "Finner ingen Auth-key, har du lagt inn en fungerende Shodan API-key?"
