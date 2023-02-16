import ipUrlFilter
import shodanFunc


def sok(inndata):
    # inndata er et array, denne kan inneholde både URL og IP

    # Filtrer ut IP-ene fra inndata
    ips = ipUrlFilter.filterUrlIp(inndata)

    # Filtrerer ut funnet IP av inndata
    url = list(set(inndata) - set(ips))

    # Gjør en shodanSearch på Url, og legger funnet IP til ips-variabelen
    searchresult = []
    for i in url:
        temp = shodanFunc.shodanSearch(i)
        searchresult.append(temp)
        ips.extend(temp[2])

    # Gjør en fullstendig søk på hver IP og skriver ut ønsket data
    hostresult = []
    if len(ips) > 0:
        for i in ips:
            hostresult.append(shodanFunc.shodanHost(i))

    # print(json.dumps(hostresult, indent=6))

    result=[]
    result.append(searchresult)
    result.append(hostresult)
    return result