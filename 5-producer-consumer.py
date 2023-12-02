# Problem: Implement a producer-consumer problem
# Challenge: How to implement it without using threads?

import time
from collections import deque
import heapq

_SENTINEL = None

class Scheduler:
    def __init__(self):
        self.ready_queue = deque()  # Ready tasks
        self.waiting_queue = []  # Sleeping tasks, priority queue
        self.sequence_number = 0  # Tie-breaker for functions with same deadline

    def call_soon(self, task: callable):
        self.ready_queue.append(task)

    def call_later(self, delay: int, task: callable):
        self.sequence_number += 1
        deadline = time.time() + delay
        heapq.heappush(self.waiting_queue, (deadline, self.sequence_number, task))

    def run(self):
        while self.ready_queue or self.waiting_queue:
            if not self.ready_queue:  # Nothing left in the ready queue
                # Find nearest deadline
                deadline, _, task = heapq.heappop(self.waiting_queue)
                delta = deadline - time.time()
                if delta > 0:
                    time.sleep(delta)  # Wait until the nearest deadline
                self.ready_queue.append(task)
            while self.ready_queue:
                func = self.ready_queue.popleft()
                func()


sched = Scheduler()  # Behind the scenes

# -------------------------- #

class AsyncQueue:
    def __init__(self):
        self.items = deque()
        self.waiting = deque()  # All getters waiting ofr data

    def put(self, item):
        self.items.append(item)
        if self.waiting:
            func = self.waiting.popleft()
            sched.call_soon(func)

    def get(self, callback: callable):
        # This is blocking. We don't know when the next item is available.
        # How can we rectify this? The whole point of async is to make it non-blocking.
        # Solution: Using callbacks!!!
        if self.items:
            callback(self.items.popleft())
        else:
            self.waiting.append(lambda: self.get(callback))


def producer(q, count):
    def _produce(n):
        if n < count:
            print("Producing: ", n)
            q.put(n)
            sched.call_later(1, lambda: _produce(n+1))
        else:
            print("Producer done!")
            q.put(_SENTINEL)

    _produce(0)


def consumer(q):
    def _consume(item):
        if item == _SENTINEL:
            print("Consumer done!")
        else:
            print("Consuming: ", item)
            sched.call_soon(lambda: consumer(q))

    q.get(_consume)


q = AsyncQueue()
sched.call_soon(lambda: producer(q, 10))
sched.call_soon(lambda: consumer(q,))
sched.run()
