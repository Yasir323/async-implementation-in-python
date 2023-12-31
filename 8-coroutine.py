import heapq
import time
from collections import deque


class Scheduler:
    def __init__(self):
        self.ready_queue = deque()  # Ready tasks
        self.current = None  # Currently running generator

    def new_task(self, coro):
        self.ready_queue.append(coro)

    def run(self):
        while self.ready_queue:
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
        time.sleep(1)
        await switch()
        n -= 1


async def countup(stop):
    n = 1
    while n <= stop:
        print("Up ", n)
        time.sleep(1)
        await switch()
        n += 1


sched.new_task(countdown(5))
sched.new_task(countup(20))
sched.run()
