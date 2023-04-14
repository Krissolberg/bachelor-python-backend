from backend.apiExtentions.shodanGetService import verifyKey, shodanDNS
from backend.apiExtentions.shodanSok import shoSok

def keyVerifier():
    return verifyKey()


def sok(inndata):
    return shoSok(inndata)


def dnsSok(domain):
    return shodanDNS(domain)


# print(json.dumps(data3, indent=6))
#if __name__ == "__main__":
    #tic = time.perf_counter()
    #print(json.dumps(sok([f'org:"Politiets IKT-tjenester (PIT)"']), indent=6))
    #print(json.dumps(sok(["www.politiet.no"]), indent=6))
# print(json.dumps(backend.apiExtentions.shodanGetService.shodanDNS('politiet.no'), indent=6))
    #tok = time.perf_counter()
    #print(f'Det tok {tok - tic:0.4f} sekunder')
# client = pymongo.MongoClient("0.0.0.0")
# print(client.server_info())
