from subprocess import Popen
from subprocess import PIPE
import urllib.request
import urllib.error
import json
import time
import sys
import re


startTime = time.time()
firstStart = True
ipCount = 0
ipList = []


def print_help():
    print('   INFORMATION:')
    print('   Made by Roman Yaschenko MO-202')
    print('   How to run: in cmd or bash type "python Tracing.py [address | ip]"')
    print('   Run example: python Tracing.py site.com')


def get_info(ip):
    url = 'http://ipinfo.io/' + ip + '/json'
    req = urllib.request.urlopen(url)
    response = json.load(req)
    return parse_info(response)


def parse_info(response):
    result = {}
    if 'org' in response:
        result['system'] = response['org'].split()[0]
        result['isp'] = response['org'].split(' ', 1)[1]
    else:
        result['system'] = 'unknown'
        result['isp'] = 'unknown'
    if 'country' in response:
        result['country'] = response['country']
    else:
        result['country'] = 'unknown'
    return result


def print_helper(number, ip, system, isp, country):
    number = format('   |  ' + "{0:<3}".format(str(number))) + '|'
    ip = format("{0:<20}".format(ip)) + '|'
    country = format("{0:<10}".format(country)) + '|'
    system = format("{0:<20}".format(system)) + '|'
    isp = format("{0:<20}".format(isp))
    print(number, ip, system, country, isp)


def get_ip_list(line):
    pattern = r'[0-9]+(?:\.[0-9]+){3}'
    global firstStart
    global ipCount
    ip = re.findall(pattern, line)
    try:
        if firstStart:
            ipList.append(ip[0])
            print('\n   Tracing has been started!\n' + '   Displaying the route for:', address, ' | ', ip[0], '\n')
            print_helper('№', 'IP ADDRESS', 'AUTONOMOUS SYSTEM', 'INTERNET SERVICE PROVIDER', 'COUNTRY')
            firstStart = False
        else:
            ipList.append(ip[0])
            response = get_info(ip[0])
            print_helper(ipCount, ip[0], **response)
            ipCount += 1
    except IndexError:
        pass


def main():
    if len(sys.argv) != 2:
        print("\n   There is no address!")
        print_help()
        return

    global address
    address = sys.argv[1]

    if sys.argv[1] == "-h" or sys.argv[1] == "--help":
        print_help()
        return

    global startTime
    lines = Popen(['tracert', address], stdout=PIPE)
    while time.time() - startTime < 30:
        startTime = time.time()
        line = lines.stdout.readline()
        if not line:
            break
        else:
            try:
                get_ip_list(str(line))
            except urllib.error.URLError:
                print('\n   Error! Check address or your internet connection!')
                break

    if len(ipList) > 0:
        if ipList[0] == ipList[len(ipList) - 1]:
            print('\n   Tracing has been completed!')
        else:
            print("\n   Something went wrong! Sorry! Try again!")
    else:
        print("\n   Error! Check address or your internet connection!")


if __name__ == '__main__':
    main()
