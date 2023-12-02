import time


def countdown(n):
    while n > 0:
        print("Down ", n)
        time.sleep(1)
        n -= 1


def countup(stop):
    n = 1
    while n <= stop:
        print("Up ", n)
        time.sleep(1)
        n += 1


# Sequential execution
countdown(5)
countup(5)

# Problem: How to do concurrency without using threads?
# Solution: Figure out a way to switch between tasks.
# Issue: We have to get rid of those loops inside the functions, once they start they block the main thread.
