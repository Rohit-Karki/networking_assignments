import nmap


def isExposedPort(url, port=80) -> bool:

    # Create an nmap scanner object
    scanner = nmap.PortScanner()

    # Specify the target host
    target_host = "example.com"  # Replace with the desired host

    # Scan the host for open ports
    scanner.scan(target_host, '80', arguments='-sS')

    # Check if port 80 is open
    return scanner[target_host].has_tcp(80)
