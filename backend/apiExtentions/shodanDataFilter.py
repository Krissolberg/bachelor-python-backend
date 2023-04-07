import ipaddress
import re

import backend.databaseFunc as dbFunc


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


def iprangesplitter(fra, til):
    split = []
    intRange = ((int(ipaddress.ip_address(til))) - int(ipaddress.ip_address(fra)))
    for j in range(intRange + 1):
        split.append(str(ipaddress.ip_address(int(ipaddress.ip_address(fra)) + j)))
    return split


def getBesDB(ports):
    dbFact = {}
    for x in ports:
        if not isinstance(x, str):
            x = str(x)
        if x != "Not found":
            dbChecker = dbFunc.findDocu('info_db', x)
            if dbChecker:
                for key1, value1 in dbChecker.items():
                    dbFact[value1['navn']] = value1['bes']
            else:
                dbFact[str(x)] = "Ingen info i db"
    return dbFact