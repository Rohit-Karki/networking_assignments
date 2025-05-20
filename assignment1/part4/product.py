import socket
import datetime
import json
from packages.http_response import HttpResponse
from packages.http_request import HttpRequest
from packages.http_params import HttpContentType, HttpMethod


class ProductWebServer:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def openConnection(self, PORT: int):

        self.sock.bind(("", PORT))
        self.sock.listen()

        while True:
            conn, addr = self.sock.accept()

            print(f"Accepted connection from {addr}")

            # conn.setblocking(False)
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                message = HttpRequest()
                message.construct_from_string(data.decode('ASCII'))
                print(message.http_method.value + " " + message.address)
                message.content_length = 0

                if message.http_method != HttpMethod.GET:
                    # print("Request is not a get request")
                    # print(data)
                    response_body = "\"Only GET method is supported\""
                    response = HttpResponse(
                        'HTTP/1.1',
                        400,
                        "Bad Request",
                        HttpContentType.JSON,
                        len(response_body.encode('ASCII')),
                        datetime.datetime.utcnow(),
                        None,
                        None,
                        response_body
                    )
                    conn.sendall(str(response).encode('ASCII'))

                if message.address[1:6] != 'product':
                    response_body = "\Only /product can be requested"
                    response = HttpResponse(
                        'HTTP/1.1',
                        404,
                        "Not Found",
                        HttpContentType.JSON,
                        len(response_body.encode('ASCII')),
                        datetime.datetime.utcnow(),
                        None,
                        None,
                        response_body
                    )
                    conn.sendall(str(response).encode('ASCII'))

                queryParams = message.address.split('?')[1]
                valuesList = queryParams.split('&')
                totalProduct = 1
                values = []
                for v in valuesList:
                    if type(v) == str:
                        response_body = "\"Query Params must be numbers\""
                        response = HttpResponse(
                            'HTTP/1.1',
                            400,
                            "Bad Request",
                            HttpContentType.JSON,
                            len(response_body.encode('ASCII')),
                            datetime.datetime.utcnow(),
                            None,
                            None,
                            response_body
                        )
                    else:
                        values.append(v.split('=')[1])
                        totalProduct *= v
                jsonValue = json.dumps({
                    "operation": "product",
                    "operands": values,
                    "result": totalProduct
                })
                response = HttpResponse(
                    'HTTP/1.1',
                    200,
                    "200 OK",
                    HttpContentType.JSON,
                    len(response_body.encode('ASCII')),
                    datetime.datetime.utcnow(),
                    None,
                    None,
                    jsonValue
                )
                conn.sendall(str(response).encode('ASCII'))
