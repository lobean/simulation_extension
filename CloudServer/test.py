__author__ = 'robin'


from multiprocessing import Process,Value,Manager,Pool
import os
import time


def processT(k, d):
    id = os.getpid()
    print "process %d %d started"% (k,id)
    d[k] = True
    i = 0
    while 1:
        i += 1
        if d[k]:
            print "process T%d is running %d times" % (k,i)
        time.sleep(2)


def main():
    d = Manager().dict()

    a = Process(target=processT, args=(1,d))
    b = Process(target=processT, args=(2,d))

    a.daemon = False
    b.daemon = False

    a.start()
    b.start()


    time.sleep(2)
    d[1]=False
    print d
    time.sleep(5)

    d[1]=True

    print d

    time.sleep(2)
    d[2] = False
    print d
    time.sleep(5)

    d[1] = False


if __name__ == "__main__":
    main()
    print "over"

