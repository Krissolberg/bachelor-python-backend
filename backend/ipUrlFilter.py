import re
def filterUrlIp(array):
    ipfilter = []
    for element in array:
        ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', element)
        if len(ip) > 0:
            ipfilter.extend(ip)
    return ipfilter