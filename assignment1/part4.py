import sys
from part4.product import ProductWebServer


def main(argv: list):
    port = int(argv[1])
    if port <= 1024:
        print("PORT must be greater than 1024")
    else:
        webServer = ProductWebServer()
        webServer.openConnection(PORT=port)


if __name__ == "__main__":
    main(sys.argv)
