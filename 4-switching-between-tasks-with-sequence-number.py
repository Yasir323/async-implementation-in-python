import time
from collections import deque
import heapq


def countdown(n):
    if n > 0:
        print("Down ", n)
        # time.sleep(4)
        sched.call_later(4, countdown, n - 1)


def countup(stop, n: int = 0):
    if n <= stop:
        print("Up ", n)
        # time.sleep(1)
        sched.call_later(1, countup, stop, n + 1)


class Scheduler:
    def __init__(self):
        self.ready_queue = deque()  # Ready tasks
        self.waiting_queue = []  # Sleeping tasks, priority queue
        self.sequence_number = 0  # Tie-breaker for functions with same deadline

    def call_soon(self, task: callable, *args):
        self.ready_queue.append((task, args))

    def call_later(self, delay: int, task: callable, *args):
        self.sequence_number += 1
        deadline = time.time() + delay
        heapq.heappush(self.waiting_queue, (deadline, self.sequence_number, task, args))

    def run(self):
        while self.ready_queue or self.waiting_queue:
            if not self.ready_queue:  # Nothing left in the ready queue
                # Find nearest deadline
                deadline, _, task, args = heapq.heappop(self.waiting_queue)
                delta = deadline - time.time()
                if delta > 0:
                    time.sleep(delta)  # Wait until the nearest deadline
                self.ready_queue.append((task, args))
            while self.ready_queue:
                func, args = self.ready_queue.popleft()
                # print(func.__name__, args)
                func(*args)


sched = Scheduler()
sched.call_soon(countdown, 5)
sched.call_soon(countup, 20)
sched.run()
