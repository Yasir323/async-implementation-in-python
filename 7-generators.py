import time
from collections import deque


class Scheduler:
    def __init__(self):
        self.ready_queue = deque()  # Ready tasks
        self.current = None

    def new_task(self, gen):
        self.ready_queue.append(gen)

    def run(self):
        while self.ready_queue:
            self.current = self.ready_queue.popleft()
            # Driver as a generator
            try:
                next(self.current)
                if self.current:
                    self.ready_queue.append(self.current)
            except StopIteration:
                pass


sched = Scheduler()


def countdown(n):
    while n > 0:
        print("Down ", n)
        time.sleep(1)
        yield
        n -= 1


def countup(stop):
    n = 1
    while n <= stop:
        print("Up ", n)
        time.sleep(1)
        yield
        n += 1


sched.new_task(countdown(5))
sched.new_task(countup(5))
sched.run()
