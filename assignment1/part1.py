import sys
from part1 import http_get_handler

def main(argv: list):
    if argv is None or len(argv) != 2:
        wrong_format()
    url = argv[1]
    if len(url) < 7 or url[0:7] != "http://":
        wrong_format()
    httpHandler = http_get_handler.HttpHandler()
    response = httpHandler.get(url=url, recursion_count=10)
    if response.body:
        for line in response.body.split('\n'):
            sys.stdout.write(str(line) + '\n')
    if response.body and response.status_code == 200:
        sys.exit(0)
    else:
        sys.stderr.write(str(response.status_code) +
                         ": " + response.reason_message)
        sys.exit(2)


def wrong_format():
    sys.stderr.write('Correct Format:\ncurl.py http://<url>')
    sys.exit(2)


if __name__ == "__main__":
    main(sys.argv)
