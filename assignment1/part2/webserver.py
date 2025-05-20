import socket
import datetime
import os
from packages.http_response import HttpResponse
from packages.http_request import HttpRequest
from packages.http_params import HttpContentType, HttpMethod


class WebServer:
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

                if message.address[:-4] != '.htm' or message.address[:-5] != '.html':
                    response_body = "\Only html or html file can be requested"
                    response = HttpResponse(
                        'HTTP/1.1',
                        403,
                        "Forbidden",
                        HttpContentType.JSON,
                        len(response_body.encode('ASCII')),
                        datetime.datetime.utcnow(),
                        None,
                        None,
                        response_body
                    )
                    conn.sendall(str(response).encode('ASCII'))

                file_name = message.address[1:]
                file_data = self.read_file(file_name)
                if file_data is None:
                    response_body = "\The file with "+file_name+" doesnot exists."
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
                else:
                    response = HttpResponse(
                        'HTTP/1.1',
                        200,
                        "200 OK",
                        HttpContentType.JSON,
                        len(response_body.encode('ASCII')),
                        datetime.datetime.utcnow(),
                        None,
                        None,
                        file_data
                    )
                    conn.sendall(str(response).encode('ASCII'))

    @staticmethod
    def read_file(file_name):
        file_name_second_option = None

        if file_name[-4:] == "html":
            # If html then also search for same filename with .htm
            file_name_second_option = file_name[:-1]
        elif file_name[-3:] == "htm":
            # If htm then also search for same filename with .html
            file_name_second_option = file_name + "l"

        file = None
        if os.path.exists('part2/files/' + file_name):
            file = open('part2/files/' + file_name, 'r')
        elif os.path.exists('part2/files/' + file_name_second_option):
            file = open('part2/files/' + file_name_second_option, 'r')

        if file:
            file_content = file.read()
            file.close()

            return file_content
        return None
