__author__ = 'luobin'

import threading
import random
import time
import socket
import multiprocessing
from multiprocessing import Queue
import logging

"""
Settings
"""

que = Queue(100000)

lock = threading.Lock()


def producer(que):
    while True:
        try:
            lock.acquire()
            que.put(random.randint(10000, 100000))
            lock.release()
        except Exception:
            print "producer error"
        time.sleep(5)


def timer(que):
    while True:
        lock.acquire()
        print 'timer', que.qsize()
        lock.release()
        time.sleep(5)


for i in range(10):
    t = threading.Thread(target=producer,args=que)
    t.setDaemon = True
    t.start()

t = threading.Thread(target=timer)
t.setDaemon = True
t.start()



class MyClient(threading.Thread):
    def __init__(self, input):
        super(MyClient, self).__init__()
        self._num = input
        self._datagram = []


def trace(self):
    num = 100  # amounts of requests to send per time
    return num


def udp_send(self, host, data):
    # host='211.69.198.200'
    address = (host, 9555)
    clisock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    clisock.sendto(data, address)


def udp_recv(self):
    # this function should be used in a new thread

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('211.69.198.223', 9555))
    data, addr = sock.recvfrom(1024)

    Log(data)  #record the response time


def load_balanbcer(self):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('211.69.198.223', 9556))
    data, addr = sock.recvfrom(1024)
    servers = {'211.69.198.**': [0, 0], '211.69.198.**': [0, 0]}

    servers[addr[0]] = data

    Log(data)  # record the response time


def run(self):
    while True:
        number = self.trace()
        for i in range(number):
            self._datagram.append(que.get())

    rate = int(self.load_balanbcer() * number)

    self.udp_send('211.69.198.200', self._datagram[0:rate])
    self.udp_send('211.69.198.200', self._datagram[rate:])


tcp_Client = MyClient()
tcp_Client.start()
tcp_Client.setDaemon = True


