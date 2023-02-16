import ipUrlFilter
import shodanFunc


def sok(inndata):
    # inndata er et array, denne kan inneholde både URL og IP
    inndata = ["politiet.no"]

    # Filtrer ut IP-ene fra inndata
    ips = ipUrlFilter.filterUrlIp(inndata)

    # Filtrerer ut funnet IP av inndata
    url = list(set(inndata) - set(ips))

    # Gjør en shodanSearch på Url, og legger funnet IP til ips-variabelen
    for i in url:
        searchresult = shodanFunc.shodanSearch(i)

    if len(searchresult) > 0:
        for i in searchresult[2]:
            ips.append(i)

    # Gjør en fullstendig søk på hver IP og skriver ut ønsket data
    hostresult = []
    if len(ips) > 0:
        for i in ips:
            hostresult.append(shodanFunc.shodanHost(i))

    # print(json.dumps(data3, indent=6))
    return hostresult
