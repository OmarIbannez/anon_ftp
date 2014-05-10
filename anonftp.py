#!/usr/bin/env python
from ftplib import FTP
import argparse
import threading


ips = {}


def anon_login(address):
    '''login with anonymous user'''
    try:
        ftp = FTP(address)
        message = ftp.login()
        ftp.quit()
        ips[address.strip()] = message
    except Exception, e:
        ips[address.strip()] = e


def main():
    '''main function where the magic happen'''
    parser = argparse.ArgumentParser(description='Selecciona una opcion')
    parser.add_argument('-ip', '--ip', type=str, help='Host to login')
    parser.add_argument('-f', '--file', type=str, help='List of ips to login')
    parser.add_argument('-o', '--output', type=str, help='Output file')
    args = parser.parse_args()

    if args.ip is not None:
        anon_login(args.ip)
    elif args.file is not None:
        try:
            ips_file = open(args.file)
            threads = []
            for ip in ips_file:
                if ip.isspace() is False:
                    t = threading.Thread(target=anon_login, args=(ip,))
                    threads.append(t)
            [x.start() for x in threads]
            [x.join() for x in threads]
            ips_file.close()
        except Exception, e:
            print e
    else:
        parser.print_help()

    if args.output is not None:
        try:
            output = open(args.output, 'w')
            for ip in ips.items():
                ip_message = 'IP: ' + ip[0] + '\n' \
                    'Message: ' + str(ip[1]) + '\n'
                output.write(ip_message)
            output.close()
        except Exception, e:
            print e
    else:
        for ip in ips.items():
            print 'IP: ' + ip[0] + '\n' \
                'Message: ' + str(ip[1]) + '\n'


if __name__ == "__main__":
    main()