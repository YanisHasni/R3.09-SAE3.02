import threading
import time

def countdown(name, start):
    count = start
    while count > 0:
        print(f"{name} : {count}")
        count -= 1
        time.sleep(0.5) 


thread1 = threading.Thread(target=countdown, args=("thread 1", 7))
thread2 = threading.Thread(target=countdown, args=("thread 2", 10))


thread1.start()
thread2.start()


thread1.join()
thread2.join()
