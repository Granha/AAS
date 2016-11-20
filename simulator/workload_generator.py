from io.io import IO
from io.io_list import IOList
from task.task import Task
from workload import Workload

class WorkloadGenerator:

    def __init__(self):
        self.state = None

    # dummy generator for initial tests
    def dummyGen(self):

        ioList1 = IOList([IO(10,5),  IO(13,7)])
        ioList2 = IOList([])

        # high priority IO instensive task
        t1 = Task("Task 1", 0, 3, 20, ioList1)

        # low priority CPU intensive task
        t2 = Task("Task 2", 10, 0, 15, ioList2)

        w = Workload([t1, t2])

        return w
    
# WorkloadGenerator
