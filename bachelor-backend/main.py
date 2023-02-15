import sys
import functions

IP = functions.shodanSearch("politiet.no")
print(IP)

for i, j in IP:
    functions.shodanHost(i)
