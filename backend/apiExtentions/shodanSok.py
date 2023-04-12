import shodan
import multiprocessing
import bisect
import backend.apiExtentions.shodanDataFilter as shodanFilter
import backend.apiExtentions.shodanGetService as shodanGet


def shoSok(inndata):
    # inndata er et array, denne kan inneholde både URL, IP og IP-range

    # Filtrering av IP og IP-range
    iprange, iprangesplit, ip = shodanFilter.filterUrlIp(inndata)

    # Filtrerer ut funnet IP og IP-range fra inndata
    url = shodanFilter.quicksort(list(set(inndata) - set(iprange) - set(ip)))

    # Initialiserer multiprocessing. Her har jeg valgt å ha 8 workers
    pool = multiprocessing.Pool(processes=8)

    # Lager individuell ip for range, og legger det i ip-array med multiprosessing
    for i in range(len(iprangesplit)):
        try:
            processes = pool.apply_async(func=shodanFilter.iprangesplitter, args=(iprangesplit[i]))
            ip.extend(processes.get())
        except:
            print("no")

    # Gjør en shodanSearch på Url, og legger funnet IP til IP-arrayet
    # Det gjøres en sortering og
    searchresult = []
    for i in url:
        try:
            temp = shodanGet.shodanSearch(i)
            searchresult.append(temp)
            sortIP = shodanFilter.quicksortIP(temp[i]['ip'])
            temp[i]['ip'] = sortIP
            temp[i]['result'] = len(sortIP)
            ip.extend(shodanFilter.quicksortIP(temp[i]['ip']))
        except shodan.APIError:
            return 'Invalid API key or you do not have access to use APIfilters in Shodan'

    # Lager individuell ip for range, og legger det i ip-array med multiprosessing
    for i in range(len(iprangesplit)):
        try:
            processes = pool.apply_async(func=shodanFilter.iprangesplitter, args=(iprangesplit[i]))
            bisect.insort(ip, processes.get())
        except:
            print("no")

    # Gjør en fullstendig søk på hver IP og skriver ut ønsket data med multiprosessing
    # Alle IP-ene blir også lagret i cache
    hostresult = []
    if len(ip) > 0:
        for i in ip:
            processes = pool.apply_async(func=shodanGet.shodanHost, args=[i])
            try:
                hostresult.append(processes.get())
            except SystemError:
                hostresult.append({i: 'No result'})

    ipResult, stat = shodanFilter.checkDB(hostresult)

    result = [searchresult, ipResult, stat]

    return result
