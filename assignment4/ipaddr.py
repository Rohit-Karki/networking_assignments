import subprocess


def getIps(url, isIpV6=False, isIpV4=False) -> list:
    response = ''
    addrs = []
    try:
        if isIpV4:
            print("nslookup" + "-type=A" + url + "8.8.8.8")
            response = subprocess.check_output(["nslookup", "-type=A", url, "8.8.8.8"],
                                               timeout=5, stderr=subprocess.STDOUT).decode("utf-8")
        elif isIpV6:
            print("nslookup" + "-type=AAAA" + url + "8.8.8.8")
            response = subprocess.check_output(["nslookup", "-type=AAAA", url, "8.8.8.8"],
                                               timeout=5, stderr=subprocess.STDOUT).decode("utf-8")
    except subprocess.CalledProcessError as e:
        print(e.output)

    address_lines = response.split("Name:")[1:]
    for address_line in address_lines:
        if ":" in address_line:
            ipaddrs = address_line.split(':', 1)[1].splitlines()
            ips = [i.strip(" \r\n\t") for i in ipaddrs]

            for ip in ips:
                if ip != '':
                    if ":" in ip and isIpV6:
                        addrs.append(ip)
                    elif "." in ip and isIpV4:
                        addrs.append(ip)
    return addrs
