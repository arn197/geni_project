from threading import Thread
from queue import Queue

qu = Queue()

def produce():
    for i in range(0, 100):
        qu.put(i)

def consume(n):
    while True:
        data = qu.get()
        print(n, data)

t = Thread(target=produce)
t.start()

p = Thread(target=consume, args=('A'))
q = Thread(target=consume, args=('B'))
p.start()
q.start()

    