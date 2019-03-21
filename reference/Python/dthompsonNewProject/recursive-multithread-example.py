import threading
import datetime
import random

exitFlag = 0


class MyThread(threading.Thread):
    def __init__(self, name, counter):
        threading.Thread.__init__(self)
        self.threadID = counter
        self.name = name
        self.counter = counter

    def run(self):
        print("\nLocking ", self.name)
        thread_lock.acquire()
        print_date(self.name, self.counter)
        thread_lock.release()
        print("Unlocking ", self.name)


def print_date(name, counter):
    date_fields = []
    today = datetime.date.today()
    date_fields.append(today)
    print("{}[{}]: {}".format(name, counter, date_fields[0]))


thread_lock = threading.Lock()
threads = []
i = 1

print("Starting threads . . . ")

while i < random.randint(10, 100):
    thread = MyThread("Thread{}".format(i), i)
    thread.start()
    threads.append(thread)
    i += 1

for t in threads:
    t.join()

print("\nFinished processing", i, "threads . . . \nExiting Program")
