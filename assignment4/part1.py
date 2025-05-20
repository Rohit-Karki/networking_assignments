import sys
import time
import json
import re
import subprocess

from ipaddr import getIps
from exposedport import isExposedPort


def main(argv: list):
    input_file_name = argv[1]
    # ouput_file_name = argv[2]
    output_dict = {}
    output_json = json.dumps({})
    with open(input_file_name) as f:
        for line in f:
            current_time = time.time()
            output_dict[line.strip()] = {
                "scan_time": current_time,
                "ipv4_addresses": getIps(line.strip(), isIpV4=True),
                "ipv6_addresses": getIps(line.strip(), isIpV6=True),
                "insecure_http": isExposedPort(line.strip()),
                "redirect_to_https": isExposedPort(line.strip())
            }
    print(output_dict)


if __name__ == "__main__":
    main(sys.argv)
