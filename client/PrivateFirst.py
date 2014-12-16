__author__ = 'luobin'

import socket


def udp_send( host, data):
    # host='211.69.198.200'
    address = (host, 9555)
    clisock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    clisock.sendto(data, address)



def requestSenderPrivateFirst():
    Upr = 200

    while 1:
        total_num = getTotalNum()
        global lock, mutex
        if mutex == 1:
            lock.acquire()
            mutex = 0

            print "thread B started"

            print "total", total_num

            if total_num > len(reqlist):
                total_num = len(reqlist)

            if total_num > Upr:
                data_local = reqlist[0:Upr]
                data_public = reqlist[Upr:total_num]
            else:
                data_local = reqlist
                data_public = []

            host1 = '211.69.198.221'
            host2 = '211.69.198.223'

            lock.release()

            udp_send(host1,str(data_local))
            udp_send(host2,str(data_public))

            print "send over"
