__author__ = 'luobin'


import socket
import threading
import time

from multiprocessing import Process

###logging###
#host_ip,request(create_time, response_time, integer)


def requestSenderPublicFirst():

    while 1:
        Upu = getTotalNum()

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

def schedule(pro):
    ex =
    varx =
    dt = ex + varx


if __name__ == "__main__":
    main()
    #processB()
    print "over"