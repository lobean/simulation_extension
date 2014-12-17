__author__ = 'luobin'

from multiprocessing import Process,Value
import time
import math
import random
import socket
import threading
import os

"""

			*hosts*
client 			211.69.198.200
private_server 	211.69.198.221
public_server	211.69.198.223

"""

reqlist=[]
lock = threading.Lock()
mutex = 0

def func(k):
    """the produce number according to double 11 curve"""
    x = [
        66.4695118366832,
        -115.427806910775,
        22.2570183935433,
        -1.26753880880697,
        58.6012004636192,
        0.207477264215836,
        881.558114828892,
        1.54185463475702
    ]
    t = 24 * float(k) / 2400  #k~(1,2400)
    num = x[0]+x[1]*t+x[2]*pow(t,2)+x[3]*pow(t,3) + x[4] * math.exp(t*x[5]) + x[6] * math.exp(-t*x[7]) + 10
    return num

def requestProducer():
    """the requests that comes"""

    clock = 1
    count = 0
    temp = 0

    while 1:
        global lock,mutex
        if mutex == 0:
            lock.acquire()
            mutex = 1

            print "thread A started"

            global reqlist
            reqlist = []


            if count % 10 == 0:
                clock += 1
                temp = func(clock)
            count += 1

            scale = random.gauss(temp,5) + 1
            reqlist = [(random.randint(1000,10000),round(time.time(),2)) for i in range(scale)]
            #print reqlist

            lock.release()
        time.sleep(1)


def udp_send(host, data):
    # host='211.69.198.200'
    address = (host, 9555)
    clisock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    clisock.sendto(data, address)

def getRate():
    """
    1.calculate the Rate and pass it to Sender
    2.Log down for every Rate decision per time t
    """
    return 0.5

def getTotalNum():
    """parameter total_num limits the most requests that can be send, others will be ????"""
    return 100

def requestSender():

    while 1:
        rate = getRate()
        total_num = getTotalNum()
        global lock, mutex
        if mutex == 1:
            lock.acquire()
            mutex = 0

            print "thread B started"

            print "total", total_num

            if total_num > len(reqlist):
                total_num = len(reqlist)

            data_local = reqlist[0:int(total_num*rate)]
            data_public = reqlist[int(total_num*rate):total_num]

            host1 = '211.69.198.221'
            host2 = '211.69.198.223'

            lock.release()

            udp_send(host1,str(data_local))
            udp_send(host2,str(data_public))

            print "send over"

        time.sleep(1)


def Log(f, message):
    try:
        f.writelines(message+'\n')

    except Exception:
        print "Log error"


def recv_item():

    fr = open("request.log",'a')
    Log(fr,str(time.ctime()))
    print "fr start"

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('127.0.0.1', 9555))
        while 1:
            print "fr write"
            data, addr = sock.recvfrom(1024)
            if not data:
                break

            print data, addr
            Log(fr, str(addr[0]) + data)
            #calculateHandleTime()#
    except Exception:
        print "fr error"

    finally:
        fr.flush()
        fr.close()

def recv_info():

    fd = open("decision.log",'a')
    Log(fd,str(time.ctime())+'\n')
    print "fd start"

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('127.0.0.1', 9666))
        while 1:
            print "fd write"
            data, addr = sock.recvfrom(1024)

            if not data:
                break

            print data, addr
            Log(fd, str(addr[0]) + data)
    except Exception:
        print "fd error"

    finally:
        fd.flush()
        fd.close()


def Recorder():
    ip_port1 = ("",9555)
    ip_port2 = ("",9666)


def scheduler():
    """
    1.receive the load information of public cloud
    2.choose whether to scale and send direction to public cloud
    3.Log down for every decision per time T
    """
    pass


def processA():

    print "A",os.getpid()

    thread_prod = threading.Thread(target=requestProducer)
    thread_send = threading.Thread(target=requestSender)

    thread_prod.start()
    thread_send.start()

    thread_prod.join()
    thread_send.join()


def processB(rate, scale):

    print "B",os.getpid()

    rate = getRate()

    thread_item = threading.Thread(target=recv_item)
    thread_info = threading.Thread(target=recv_info)

    thread_info.setDaemon(False)
    thread_item.setDaemon(False)

    thread_item.start()
    thread_info.start()

    thread_item.join()
    thread_info.join()

def main():
    rate = Value('d',0.5)
    scale = Value('i',100)

    a = Process(target=processA, args=(rate,scale))
    b = Process(target=processB, args=(rate,scale))

    a.daemon = True
    b.daemon = True

    a.start()
    b.start()

    a.join()
    b.join()


if __name__ == "__main__":
    main()
    print "main",os.getpid()
    print "over"


