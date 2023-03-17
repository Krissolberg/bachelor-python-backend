import multiprocessing

import shodan

import backend.apiExtentions.shodanDataFilter as shodanFilter
import backend.apiExtentions.shodanGetService
import backend.apiExtentions.shodanGetService as shodanGet

import time
import json

def keyVerifier():
    return shodanGet.verifyKey()
def sok(inndata):
    # inndata er et array, denne kan inneholde både URL, IP og IP-range

    # Filtrering av IP og IP-range
    iprange, iprangesplit, ip = shodanFilter.filterUrlIp(inndata)

    # Filtrerer ut funnet IP og IP-range fra inndata
    url = list(set(inndata) - set(iprange) - set(ip))

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
    searchresult = []
    for i in url:
        try:
            temp = shodanGet.shodanSearch(i)
            searchresult.append(temp)
            ip.extend(temp[i]['ip'])
        except shodan.APIError:
            return 'Invalid API key or you do not have access to use APIfilters in Shodan'

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

    result = [searchresult, hostresult]
    return result

def dnsSok(domain):
    return backend.apiExtentions.shodanGetService.shodanDNS(domain)

# print(json.dumps(data3, indent=6))
if __name__ == "__main__":
    tic = time.perf_counter()
    #print(json.dumps(sok(['org:"Politiets IKT-tjenester (PIT)"']), indent=6))
    print(json.dumps(backend.apiExtentions.shodanGetService.shodanDNS('politiet.no'), indent=6))
    tok = time.perf_counter()
    print(f'Det tok {tok - tic:0.4f} sekunder')

