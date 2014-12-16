__author__ = 'robin'

import socket
from multiprocessing import  Queue
import math
import time

que=Queue(10000)


def isPrime(elem):
    for i in range(2, math.sqrt(elem)):
        if elem % i == 0:
            return False
    return True


def udp_send(host, port, data):
    # host='211.69.198.200'
    address = (host, port)
    clisock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    clisock.sendto(data, address)


def recv_items(que):

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('localhost', 9555))
        while 1:
            data, addr = sock.recvfrom(6400)
            items = eval(data)
            for i in range(len(items)):
                que.put(items[i])

    except Exception:
        print "error"


def handle(que,i):

    k = 0
    sum = 0

    while 1:

        item = eval(que.get())
        res = isPrime(item[0])
        cur = round(time.time(),2)
        data = str((item[0],item[1],cur,res))
        udp_send("211.69.198.38",9555,data)

        k += 1
        acc = cur - item[1]
        sum += acc
        if k % 5 == 0:
            handle_time = sum / 5.0
            sum = 0
            k = 0

        time.sleep(1)