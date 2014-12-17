__author__ = 'robin'

import socket
from multiprocessing import  Queue
import threading
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

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        sock.bind(('localhost', 9555))
        while 1:
            data, addr = sock.recvfrom(6400)
            items = eval(data)
            if items == '0':
                break

            for i in range(len(items)):
                que.put(items[i])

    except Exception:
        print "error"
    finally:
        sock.close()

handle_time = 0

def handle(que):

    k = 0
    sum = 0

    while 1:
        try:
            item = eval(que.get())
        except Exception:
            print "Queue Empty"
        res = isPrime(item[0])
        cur = round(time.time(),2)
        data = str((item[0],item[1],cur,res))
        udp_send("211.69.198.38",9555,data)

        k += 1
        acc = cur - item[1]
        sum += acc
        if k % 5 == 0:
            global handle_time
            handle_time = sum / 5.0
            sum = 0
            k = 0

        time.sleep(1)

def send_info(que):

    host = "211.69.198.200"

    try:
        while 1:
            size = que.qsize()
            global  handle_time
            data = str((size,handle_time))
            udp_send(host,9666,data)
            time.sleep(2)

    except Exception:
        print "error"

def main():
    thread_recv = threading.Thread(target=recv_items,args=(que,))
    thread_hand = threading.Thread(target=handle,args=(que,))
    thread_send = threading.Thread(target=send_info,args=(que,))

    thread_recv.start()
    thread_hand.start()
    thread_send.start()

    thread_recv.join()
    thread_hand.join()
    thread_send.join()


if __name__ == "__main__":
    main()
    print "over"