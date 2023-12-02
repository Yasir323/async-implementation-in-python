import time
from collections import deque
import heapq


def countdown(n):
    if n > 0:
        print("Down ", n)
        time.sleep(4)
        sched.call_soon(countdown, n - 1)


def countup(stop, n: int = 0):
    if n <= stop:
        print("Up ", n)
        time.sleep(1)
        sched.call_soon(countup, stop, n + 1)


class Scheduler:
    def __init__(self):
        self.ready_queue = deque()  # Ready tasks

    def call_soon(self, task: callable, *args):
        self.ready_queue.append((task, args))

    def run(self):
        while self.ready_queue:
            func, args = self.ready_queue.popleft()
            # print(func.__name__, args)
            func(*args)


sched = Scheduler()
sched.call_soon(countdown, 5)
sched.call_soon(countup, 5)
sched.run()

# Problem: If one task takes a long amount of time, it will block the main thread.
# We can simulate that by increasing the sleep time of one or both of the tasks.
# Solution: If there is IO operation like sleep we have to switch the moment sleep starts.
# We can implement a function like call later and pass in the delay explicitly.
