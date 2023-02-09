import sys
import functions

input = sys.argv[1]

functions.shodanSearch(input)
IP = functions.shodanSearch(input)
print(IP)

for i in IP:
    functions.shodanHost(i)