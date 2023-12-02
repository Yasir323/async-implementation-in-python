import heapq
import time
from collections import deque


class Scheduler:
    def __init__(self):
        self.ready_queue = deque()  # Ready tasks
        self.current = None  # Currently running generator
        self.sleeping = []
        self.sequence_number = 0

    async def sleep(self, delay):
        deadline = time.time() + delay
        self.sequence_number += 1
        heapq.heappush(self.sleeping, (deadline, self.sequence_number, self.current))
        self.current = None  # Disappear
        await switch()  # Switch to a different task, if any

    def new_task(self, coro):
        self.ready_queue.append(coro)

    def run(self):
        while self.ready_queue or self.sleeping:
            if not self.ready_queue:
                deadline, _, coro = heapq.heappop(self.sleeping)
                delta = deadline - time.time()
                if delta > 0:
                    time.sleep(delta)
                self.ready_queue.append(coro)

            self.current = self.ready_queue.popleft()
            # Driver as a generator
            try:
                self.current.send(None)  # Send to a coroutine
                if self.current:
                    self.ready_queue.append(self.current)
            except StopIteration:
                pass


sched = Scheduler()

# ------------------------------------------- #

class Awaitable:
    def __await__(self):
        yield


def switch():
    return Awaitable()


async def countdown(n):
    while n > 0:
        print("Down ", n)
        await sched.sleep(4)
        n -= 1


async def countup(stop):
    n = 1
    while n <= stop:
        print("Up ", n)
        await sched.sleep(1)
        n += 1


sched.new_task(countdown(5))
sched.new_task(countup(20))
sched.run()
