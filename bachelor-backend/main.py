import sys
import functions

IP = functions.shodanSearch("politiet.no")

ips = []
for i, j in IP:
    ips.append(i)

functions.shodanHost(ips)
