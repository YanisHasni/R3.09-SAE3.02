import threading
import time

def thread1():
    for i in range (5):
        print("Je suis la thread 1")
        time.sleep(0.5)

def thread2():
    for i in range (5):
        print("Je suis la thread 2")
        time.sleep(0.5)

start = time.perf_counter()

t1 = threading.Thread(target=thread1)
t1.start()

t2 = threading.Thread(target=thread2)
t2.start()

t1.join()
t2.join()

end = time.perf_counter() 
print(f"Tasks ended in {round(end - start, 2)} second(s)")


