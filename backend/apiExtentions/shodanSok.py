from multiprocessing import Pool
from backend.apiExtentions.shodanGetService import shodanSearch, shodanHost
from backend.apiExtentions.shodanDataFilter import filterUrlIp, quicksort, iprangesplitter, quicksortIP, checkDB


def shoSearch(ipUrlInput):
    """
     Input is a string array, which can include URL, single IP and IP-range.
     We start with filterering single IPs and IP-ranges. Then take the remaining as URLs, and sort them A-Z.

     We then continue with creating single IPs for each IP-ranges and add those to single IP list.
     We do the same thing with URLs, but add the single IPs to their unique array.

     At last, we do the IP search.
    """

    searchresult, ipurl, hostresult = [], [], []
    pool = Pool(processes=8)
    iprange, iprangesplit, ip = filterUrlIp(ipUrlInput)

    url = quicksort(list(set(ipUrlInput) - set(iprange) - set(ip)))

    for i in range(len(iprangesplit)):
        processes = pool.apply_async(func=iprangesplitter, args=(iprangesplit[i]))
        ip.extend(processes.get())

    for i in url:
        try:
            temp = shodanSearch(i)
            searchresult.append(temp)
            sortIP = quicksortIP(temp[i]['ip'])
            temp[i]['ip'] = sortIP
            temp[i]['result'] = len(sortIP)
            ipurl.extend(quicksortIP(temp[i]['ip']))
        except:
            return 'Invalid API key or you do not have access to use APIfilters in Shodan'

    if len(ip) > 0 or len(ipurl):
        ip = quicksortIP(ip)
        for i in ipurl:
            processes = pool.apply_async(func=shodanHost, args=[i])
            try:
                hostresult.append(processes.get())
            except:
                hostresult.append({i: 'No result'})
        for i in ip:
            processes = pool.apply_async(func=shodanHost, args=[i])
            try:
                hostresult.append(processes.get())
            except:
                hostresult.append({i: 'No result'})

    ipResult, stat = checkDB(hostresult)

    result = [searchresult, ipResult, stat]

    return result
