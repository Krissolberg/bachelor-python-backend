import re

from shodan import Shodan
from backend import cacheService

auth = "wqBocETm9zujq2lWjSaYFUOFBhXDqeHV"


def verifyShodanKey():
    return cacheService.nosession.get(f'https://api.shodan.io/api-info?key={auth}', timeout=3,
                                      headers={'Cache-Control': 'no-cache, no-store'}).json()


def shodanDNS(domain):
    return Shodan(auth).dns.domain_info(domain=domain, history=False, type=None, page=1)


def shodanSearch(indata):
    results, limit, counter = [], 200, 0

    for x in Shodan(auth).search_cursor(indata):

        results.append(x)
        counter += 1
        if counter >= limit:
            break

    return {indata: {
        'ip': [result['ip_str'] for result in results],
        'org': [result['org'] for result in results]}}


def shodanHost(ips):
    try:
        host = (cacheService.session.get(
            f'https://api.shodan.io/shodan/host/{ips}?key={auth}').json())
        for item in host['data']:
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
                if not vulns:
                    vulns = "Not found"
            except:
                vulns = "Not found"

        return {host['ip_str']: {'org': host['org'],
                                 'os': host['os'],
                                 'hostnames': host['hostnames'],
                                 'domains': host['domains'],
                                 'ports': host['ports'],
                                 'versions': versions,
                                 'cipher': cipher,
                                 'vulns': vulns}}

    except:
        raise SystemError("noresult")
