from shodan import APIError
from multiprocessing import Pool
from backend.apiExtentions.shodanDataFilter import filterUrlIp, quicksort, iprangesplitter, quicksortIP, checkDB
from backend.apiExtentions.shodanGetService import shodanSearch, shodanHost


def shoSok(inndata):
    # inndata er et array, denne kan inneholde både URL, IP og IP-range

    # Filtrering av IP og IP-range
    iprange, iprangesplit, ip = filterUrlIp(inndata)

    # Filtrerer ut funnet IP og IP-range fra inndata
    url = quicksort(list(set(inndata) - set(iprange) - set(ip)))

    # Initialiserer multiprocessing. Her har jeg valgt å ha 8 workers
    pool = Pool(processes=8)

    # Lager individuell ip for range, og legger det i ip-array med multiprosessing
    for i in range(len(iprangesplit)):
        try:
            processes = pool.apply_async(func=iprangesplitter, args=(iprangesplit[i]))
            ip.extend(processes.get())
        except:
            print("no")

    # Gjør en shodanSearch på Url, og legger funnet IP til IP-arrayet
    # Det gjøres en sortering og
    searchresult = []
    ipUrl = []
    for i in url:
        try:
            temp = shodanSearch(i)
            searchresult.append(temp)
            sortIP = quicksortIP(temp[i]['ip'])
            temp[i]['ip'] = sortIP
            temp[i]['result'] = len(sortIP)
            ipUrl.extend(quicksortIP(temp[i]['ip']))
        except APIError:
            return 'Invalid API key or you do not have access to use APIfilters in Shodan'

    # Gjør en fullstendig søk på hver IP og skriver ut ønsket data med multiprosessing
    # Alle IP-ene blir også lagret i cache
    hostresult = []
    if len(ip) > 0 or len(ipUrl):
        ip = quicksortIP(ip)
        for i in ipUrl:
            processes = pool.apply_async(func=shodanHost, args=[i])
            try:
                hostresult.append(processes.get())
            except SystemError:
                hostresult.append({i: 'No result'})
        for i in ip:
            processes = pool.apply_async(func=shodanHost, args=[i])
            try:
                hostresult.append(processes.get())
            except SystemError:
                hostresult.append({i: 'No result'})

    ipResult, stat = checkDB(hostresult)

    result = [searchresult, ipResult, stat]

    return result
