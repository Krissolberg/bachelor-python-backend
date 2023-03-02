import ipaddress
import json

import ipUrlFilter
import shodanFunc


def sok(inndata):
    # inndata er et array, denne kan inneholde både URL og IP

    # Filtrer ut IP-ene fra inndata
    iprange, iprangesplit, ip = ipUrlFilter.filterUrlIp(inndata)

    # Filtrerer ut funnet IP av inndata
    url = list(set(inndata) - set(iprange)-set(ip))

    for i in iprangesplit:
        intRange = ((int(ipaddress.ip_address(i[1])))-int(ipaddress.ip_address(i[0])))
        for j in range(intRange):
            ip.append(str(ipaddress.ip_address(int(ipaddress.ip_address(i[0]))+j)))

    print(ip)

    # Gjør en shodanSearch på Url, og legger funnet IP til ips-variabelen
    searchresult = []
    for i in url:
        temp = shodanFunc.shodanSearch(i)
        searchresult.append(temp)
        ip.extend(temp[i]['ip'])

    # Gjør en fullstendig søk på hver IP og skriver ut ønsket data
    hostresult = []
    if len(ip) > 0:
        for i in ip:
            try:
                hostresult.append(shodanFunc.shodanHost(i))
            except:
                print(f'ingenting i {i}')




    # print(json.dumps(hostresult, indent=6))

    result = [searchresult, hostresult]
    return result


# print(json.dumps(data3, indent=6))

print(json.dumps(sok(["163.174.115.35-163.174.115.45"]), indent=6))
