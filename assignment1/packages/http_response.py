import datetime
from packages.http_params import getHeaderFromString, HttpContentType


class HttpResponse:
    http_version = None
    status_code = None
    reason_message = None

    content_type = None
    content_length = None

    location = None

    host = None
    body = None
    date = None

    def __init__(self, http_version: str = None, status_code: int = None, reason_message: str = None,
                 content_type: HttpContentType = None, content_length: int = None, date: datetime = None,
                 location: str = None,
                 host: str = None, body=None):
        self.http_version = http_version
        self.status_code = status_code
        self.reason_message = reason_message
        self.content_type = content_type
        self.content_length = content_length
        self.location = location
        self.host = host
        self.body = body
        self.date = date

    def __str__(self):
        return (self.http_version + str(self.status_code) + " " + self.reason_message) + \
            (('\r\Host: ' + self.host) if (self.host is not None) else "") + \
            (('\r\Location: ' + self.location) if (self.location is not None) else "") + \
            (('\r\nContent-Type: ' + self.content_type.value) if (self.content_type is not None) else "") + \
            (('\r\nContent-Length: ' + str(self.content_length))) + \
            (('\r\nDate: ' + self.date.strftime("%a, %d %b %Y %H:%M:%S") + " GMT") if (
                self.date is not None) else "") + \
            (('\r\n\r\n' + self.body) if (self.body is not None) else "")

    def from_string(self, message: str):
        lines = message.split(b'\r\n')
        response_line = lines[0]
        self.http_version = response_line.split(b" ")[0]
        print(self.http_version)
        self.status_code = response_line.split(b" ")[1]
        self.reason_message = b' '.join(response_line.split(b" ")[2:])

        isBodyStarted = False
        body = b''

        for line in lines:
            if isBodyStarted:
                body += line+b'\n'
            else:
                if b"" in line:
                    isBodyStarted = True
                else:
                    header = getHeaderFromString(line)
                    httpContentType = HttpContentType.unknown
                    if header.key == "Content-Type":
                        try:
                            self.content_type = httpContentType.from_string(header.value.split(';')[
                                0])
                        except:
                            self.content_type = HttpContentType.unknown
                    elif header.key == "Content-Length":
                        try:
                            self.content_length = int(header.value)
                        except:
                            print("Could not parse content length from header:\n" +
                                  header.key + ":" + header.value)
        if len(body) > 0:
            self.body = body[:-1]
