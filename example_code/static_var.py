import time

def func():
    if func.counter > 8:
        func.counter = 0
    else:
        func.counter += 1
    return func.counter

func.counter = 0

while True:
    print(func())
    time.sleep(1)
