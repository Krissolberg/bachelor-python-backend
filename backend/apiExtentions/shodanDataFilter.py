import ipaddress
import re

import backend.databaseFunc as dbFunc


def filterUrlIp(array):
    iprange, iprangesplit, ip = [], [], []
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


def iprangesplitter(fra, til):
    intRange = ((int(ipaddress.ip_address(til))) - int(ipaddress.ip_address(fra)))
    return [str(ipaddress.ip_address(int(ipaddress.ip_address(fra)) + j)) for j in range(intRange + 1)]


def quicksort(array):
    min, lik, stor = [], [], []

    if len(array) > 1:
        pivot = array[0]
        for x in array:
            if x < pivot:
                min.append(x)
            elif x == pivot:
                lik.append(x)
            elif x > pivot:
                stor.append(x)
        return quicksort(min) + lik + quicksort(stor)
    else:
        return array


def quicksortIP(array):
    intArray = quicksort(list(set([int(ipaddress.ip_address(i)) for i in array])))
    return [str(ipaddress.ip_address(i)) for i in intArray]


def getBesDB(inn, col):
    dbFact = {}
    if inn == "Not found":
        return [dbFact]
    for x in inn:
        if not isinstance(x, str):
            x = str(x)
        dbChecker = dbFunc.findOne('info_db', x, col)
        if dbChecker:
            try:
                dbFact[dbChecker['navn']] = dbChecker['bes']
            except:
                dbFact[str(x)] = "Feil i db"
        else:
            dbFact[str(x)] = "Ingen info i db"
    return dbFact


def checkDB(hostresult):
    port, portBesTotal, version, vuln = {}, {}, {'tekst': {}}, {}

    for x in range(len(hostresult)):
        for key, value in hostresult[x].items():
            if value == "No result":
                continue
            ports, versions, vulns = value['ports'], value['versions'], value['vulns']

            portBes = getBesDB(ports, 'portBes')
            portBesTotal.update(portBes)
            if portBes != [{}]:
                value['ports'] = portBes
            else:
                value['ports'] = "Not found"
            for x in ports:
                port.update({f'{x}': port.get(f'{x}', 0) + 1})

            versionBes = getBesDB(versions, 'versionsBes')
            if versionBes != [{}]:
                value['versions'] = versionBes
            else:
                value['versions'] = "Not found"
            if versions != "Not found":
                version.update({f'{versions}': version.get(f'{versions}', 0) + 1})
            else:
                version.update({'Not found': version.get('Not found', 0) + 1})

            vulnsBes = getBesDB(vulns, 'vulnsBes')
            if vulnsBes == [{}]:
                value['vulns'] = "Not found"
            else:
                value['vulns'] = vulnsBes
            if vulns != "Not found":
                for x in vulns:
                    vuln.update({f'{x}': vuln.get(f'{x}', 0) + 1})
            else:
                vuln.update({'Not found': vuln.get('Not found', 0) + 1})

    for v in version.keys():
        if v != "Not found" and v != "tekst":
            version["tekst"].update({f'{v}': dbFunc.findOne('info_db', v, 'versionBes')})
    try:
        if version["['TLSv1', 'SSLv2', 'SSLv3', 'TLSv1.1', 'TLSv1.2', 'TLSv1.3']"] > \
                version["['TLSv1', 'SSLv2', 'SSLv3', 'TLSv1.1', 'TLSv1.2']"]:
            version["tekst"].update({'lederTekst': "nesten1.3"})
    except:
        version["tekst"].update({'lederTekst': "vet ikke"})

    port['total'] = sum(port.values())
    port.update({'tekst': portBesTotal})

    stat = {'stats': {'ports': port, 'versions': version, 'vulns': vuln}}
    return hostresult, stat
