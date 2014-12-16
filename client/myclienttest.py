__author__ = 'luobin'

import socket

def udp_send(host, port, data):
    # host='211.69.198.200'
    address = (host, port)
    clisock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    clisock.sendto(data, address)


def test():
    host = "127.0.0.1"
    data1 = ""
    data2 = ""
    udp_send(host,9555,data1)
    udp_send(host,9666,data2)


if __name__ == "__main__":
    test()

