from packages.http_params import HttpMethod, getHeaderFromString, HttpContentType


class HttpRequest:
    http_method = None
    address = None
    http_version = None

    content_type = None
    content_length = None

    host = None
    body = None

    def __init__(self, http_method: HttpMethod = None, address: str = None, http_version: str = None,
                 content_type: HttpContentType = None, content_length: int = None,
                 host: str = None, body=None):
        self.http_method = http_method
        self.address = address
        self.http_version = http_version
        self.host = host
        self.content_type = content_type
        self.content_length = content_length
        self.body = body

    def __str__(self) -> str:
        return (self.http_method.value + " " + self.address+" " + self.http_version) + \
            (("\r\nHost: "+self.host) if (self.host is not None) else "") + \
            (('\r\nContent-Type: ' + self.content_type.value) if (self.content_type is not None) else "") + \
            (('\r\nContent-Length: ' + str(self.content_length)) if (self.content_length is not None) else "") + \
            (('\r\n\r\n' + self.body + "\r\n\r\n")
             if (self.body is not None) else "")

    def construct_from_string(self, message):
        lines = message.split('\r\n')

        # Initializing a get request
        method_line = lines[0]
        if " " not in method_line:
            return True
        http_method = HttpMethod.unknown
        try:
            self.http_method = http_method.from_string(
                method_line.split(' ')[0].strip())
        except:
            self.http_method = HttpMethod.unknown
            print(self.http_method.value)
        self.address = method_line.split(' ')[1]
        self.host = method_line.split(' ')[2]

        isBodyStarted = False
        body = ''
        for line in lines:
            if isBodyStarted:
                body += line
            else:
                if line == "":
                    isBodyStarted = True
                else:
                    header = getHeaderFromString(line)
                    if header.key == "Content-Type":
                        content_type = header.value
                    elif header.key == "Content-Length":
                        try:
                            content_length = int(header.value)
                        except:
                            print("Could not parse content length from header:\n" +
                                  header.key + ":" + header.value)
                    elif header.key == "Host":
                        self.host = header.value
