import time
from threading import Thread


def hello_doe():
    time.sleep(3)
    print('Wait a moment...\nHave a great day!')


t = Thread(target=hello_doe)

print('Hello, John Doe!')
t.start()
