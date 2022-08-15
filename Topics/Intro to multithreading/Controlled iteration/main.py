from threading import Thread
import time

def num():
    for i in range(1, 6):
        print("The number is: ", i)
        time.sleep(1)

def double_num():
    for i in range(1, 6):
        print("The double of the number is: ", i * 2)
        time.sleep(1)

def square_num():
    for i in range(1, 6):
        print("The square of the number is: ", i ** 2)
        time.sleep(1)

thread_1 = Thread(target=num)
thread_2 = Thread(target=double_num)
thread_3 = Thread(target=square_num)

thread_1.start()
time.sleep(0.2)
thread_2.start()
time.sleep(0.2)
thread_3.start()