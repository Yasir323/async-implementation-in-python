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


class QueueClosed(Exception):
    pass

class Awaitable:
    def __await__(self):
        yield


def switch():
    return Awaitable()


class AsyncQueue:
    def __init__(self):
        self.items = deque()
        self.waiting = deque()
        self.is_closed = False

    def close(self):
        self.is_closed = True
        if self.waiting and not self.items:
            sched.ready_queue.append(self.waiting.popleft())  # Reschedule waiting tasks

    async def put(self, item):
        if self.is_closed:
            raise QueueClosed()

        self.items.append(item)
        if self.waiting:
            sched.ready_queue.append(self.waiting.popleft())

    async def get(self):
        while not self.items:
            if self.is_closed:
                raise QueueClosed()
            self.waiting.append(sched.current)  # Put myself to sleep
            sched.current = None                # Disappear
            await switch()                      # Switch to another task
        return self.items.popleft()


async def producer(q, count):
    for n in range(count):
        print("Producing: ", n)
        await q.put(n)
        await sched.sleep(1)
    print("Producer done!")
    q.close()

async def consumer(q):
    try:
        while True:
            item = await q.get()
            print("Consumed: ", item)
    except QueueClosed:
        pass
    print("Consumer done!")


q = AsyncQueue()
sched.new_task(producer(q, 10))
sched.new_task(consumer(q))
sched.run()
