import threading
import time

def thread(name, count):
    for i in range (count):
        print(f"Je suis la thread {name}")
        time.sleep(0.5)

start = time.perf_counter()

t1 = threading.Thread(target=thread, args=[1,9])
t1.start()

t2 = threading.Thread(target=thread, args=[2,8])
t2.start()

t1.join()
t2.join()

end = time.perf_counter() 
print(f"Tasks ended in {round(end - start, 2)} second(s)")


