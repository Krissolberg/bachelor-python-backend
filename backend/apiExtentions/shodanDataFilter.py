import re


def filterUrlIp(array):
    iprange = []
    iprangesplit = []
    ip = []
    for element in array:
        ipr = re.findall(r'(?:(?:\d|[01]?\d\d|2[0-4]\d|25[0-5])\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d|\d)(?:\/\d{1,'
                         r'2})?-(?:(?:\d|[01]?\d\d|2[0-4]\d|25[0-5])\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d|\d)(?:\/\d{1,'
                         r'2})?', element)
        ips = re.findall(r'[0-9]+(?:\.[0-9]+){3}', element)
        if len(ipr) > 0:
            iprange.extend(ipr)
            ra1, ra2 = ipr[0].split("-")
            iprangesplit.append([ra1, ra2])
        elif len(ips) > 0:
            ip.extend(ips)
    return [iprange, iprangesplit, ip]


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
