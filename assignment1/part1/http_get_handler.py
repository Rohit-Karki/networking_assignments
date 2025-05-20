# CURL Clone in Python

import socket
import sys
from packages.http_params import HttpMethod, HttpContentType
from packages.http_request import HttpRequest
from packages.http_response import HttpResponse


class HttpHandler:
    sock = None

    def get(self, url, recursion_count=0) -> HttpResponse:
        if (url[:7] != "http://"):
            return HttpResponse("1.1.", 401, "The protocol is https")
        url_arr = url.split("/")
        base = url_arr[2]
        addr = ('/').join(url_arr[3:])
        port = 80

        if (base.find(':') != -1):
            split_base = base.split(':')
            base = split_base[0]
            port = int(split_base[1])
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(3)
        self.sock.connect((base, port))

        request = HttpRequest(http_method=HttpMethod.GET,
                              address='/' + addr,
                              http_version="HTTP/1.1",
                              host=base)
        print(request)
        self.sock.sendall(str(request).encode("ASCII"))
        body_length = None
        content_length = None
        response_raw = b''
        response = HttpResponse()

        # If the body is not present in the response then there will be no body length until there is a body length the request is taking place
        # If there is no content length then the request is taking place until the server closes the connection or the while loop is broken if there is no data

        while body_length is None or (content_length is not None and body_length < content_length) or content_length is None:
            try:
                new_data = self.sock.recv(4096)
                print(new_data)
            except:
                break

            if new_data == b'':
                break

            if content_length is None and body_length is None \
                    and HttpContentType.HTML.value.encode("ASCII") not in new_data:
                return HttpResponse(status_code=400, reason_message="Content Type is not text/html")

            response_raw += new_data
            # print(str(response_raw))
            response.from_string(response_raw)

            if response.content_type != HttpContentType.HTML.value:
                return HttpResponse(status_code=400, reason_message="Content type is not text/html")

            content_length = response.content_length
            body_length = len(response_raw.split(b'\r\n\r\n')[1])

        self.sock.close()
        response = HttpResponse()

        response.from_string(response_raw)

        if response.content_type is None:
            return HttpResponse(status_code=400, reason_message="Content-Type header not found")
        if response.content_type is not HttpContentType.html:
            return HttpResponse(status_code=400, reason_message="Content type is not text/html")

        if response.status_code == 301 or response.status_code == 302:
            if response.location is None:
                return HttpResponse(status_code=400, reason_message="Redirection failed, Location header not found")
            sys.stderr.write("Redirected to: " + response.location + '\n')
            return self.get(response.location, recursion_count=recursion_count + 1)


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
