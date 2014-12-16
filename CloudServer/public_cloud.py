__author__ = 'robin'

from multiprocessing import Queue, Process, Value, Manager, Pool
import socket
import math
import time


cur_proc = 0


def recv_items(que):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.bind(('localhost', 9555))
        while 1:
            data, addr = sock.recvfrom(64000)
            items = eval(data)
            for i in range(len(items)):
                que.put(items[i])

    except Exception:
        print "error"

    finally:
        sock.close()


def adjust(direct,d):
    global  cur_proc

    if direct == 1:
        cur_proc += 1
        d[cur_proc] = True
    elif direct == -1:
        d[cur_proc] = False
        cur_proc -= 1
    else:
        pass


def recv_info(que,d):

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:

        sock.bind(('localhost', 9666))
        while 1:
            data, addr = sock.recvfrom(1024)
            direct = data
            adjust(direct,d)

            time.sleep(2)


    except Exception:
        print "error"

    finally:
        sock.close()


def udp_send(host, port, data):
    # host='211.69.198.200'
    address = (host, port)
    clisock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    clisock.sendto(data, address)
    clisock.close()



def send_info(que):

    global cur_proc
    host = "211.69.198.200"

    try:
        while 1:
            size = que.qsize()

            data = (cur_proc,size)
            udp_send(host,9666,data)

            time.sleep(2)

    except Exception:
        pass

def isPrime(elem):
    for i in range(2, math.sqrt(elem)):
        if elem % i == 0:
            return False
    return True



def handle(que,i,d):

    k = 0
    sum = 0
    d[i] = False

    while 1:
        if  d[i]:
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





def main():
    manager = Manager()
    d = manager.dict()
    que=Queue(10000)

    p = Process(recv_items(que))
    p.daemon = True
    p.start()


    pool = Pool(100)
    for i in range(1,100):
        pool.apply_async(handle,args=(que,i,d))

    p.join()

    que.join()

if __name__ == "__main__":
    main()