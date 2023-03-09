import shodan
import backend.apiExtentions.shodanDataFilter as shodanFilter
from backend import cacheService

auth = ""

def shodanSearch(indata):
    ip, org = [], []

    results = shodan.Shodan(auth).search(indata)

    for result in results['matches']:
        try:
            ip.append(result['ip_str'])
        except:
            break
        try:
            org.append(result['org'])
        except:
            break

    data = {indata: {'result': results['total'],
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

        # print(json.dumps(data, indent=6))

        return data
    except:
        raise SystemError("noresult")
