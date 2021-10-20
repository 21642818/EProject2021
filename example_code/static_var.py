import time

def func():
    if func.counter >= 7:
        func.counter = 0
    else:
        func.counter += 1
    return func.counter

func.counter = -1

while True:
    print(func())
    time.sleep(1)
