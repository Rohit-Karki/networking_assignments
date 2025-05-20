from enum import Enum


class HttpMessageHeader:
    key = None
    value = None

    def __init__(self, key, value):
        self.key = key
        self.value = value


class HttpMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    unknown = "unknownmethod"

    def from_string(self, value):        
        if value == self.GET.value:
            return self.GET
        elif value == self.POST.value:
            return self.POST
        elif value == self.PUT.value:
            return self.PUT
        elif value == self.DELETE.value:
            return self.DELETE
        else:
            return self.unknown


class HttpContentType(Enum):
    JSON = "json/application"
    HTML = "text/html"
    unknown = "unknown"

    def from_string(self, value):
        if value == self.JSON.value:
            return self.JSON
        elif value == self.HTML.value:
            return self.HTML
        else:
            return self.unknown


class QueryParameter:
    parameter = None
    value = None

    def __init__(self, parameter, value):
        self.parameter = parameter
        self.value = value


def getHeaderFromString(string):
    str_split = string.split(' ')
    if (len(str_split) >= 2):
        header_key = str_split[0][:-1]
        header_value = " ".join(str_split[1:])
        return HttpMessageHeader(header_key, header_value)
    else:
        return HttpMessageHeader(None, None)
