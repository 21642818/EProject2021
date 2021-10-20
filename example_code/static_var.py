from typing import Counter


import time

def func():
    func.counter = 0
    if func.counter >= 8:
        func.counter = 0
    else:
        func.counter += 1
    return func.counter

print(func)
time.sleep(1)
