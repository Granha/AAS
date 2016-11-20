from simulator.processor import Processor

# Events
from simulator.task_creation_event import TaskCreationEvent
from simulator.task_creation_event import TaskFinishEvent
from simulator.io_start_event import IOStartEvent
from simulator.io_complete_event import IOCompleteEvent

import sys

# System Simulator
class Simulator:

    def __init__(self, scheduler):
        self.scheduler = scheduler
        self.workload = None
        self.processor = Processor()        
        self.scheduler.setProcessor(self.processor)

    def setWorkload(self, workload):
        self.workload = workload
        return None
    
    def run(self):                
        # initialize event queue with creation
        initialEvents = self.workload.getInitialEvent()
        queue = EventQueue(initialEvents)

        # number of alive tasks
        nTasks = queue.getSize()

        # there are no tasks
        if nTasks == 0:
            return
        
        # first timer event
        timerEvent = TimerEvent(1)
        queue.addEvent(timerEvent)        

        # Main Loop
        while not isEmpty(queue):
            event = queue.extractMin()

            # time can be an arbitrary real number
            self.processor.setTime(event.getTime())
            
            if isinstance(event, TimerEvent):
                print "Timer Event"

                # tick is only integer
                self.processor.setTicks(event.getTicks())

                # inform scheduler of timer interrupt
                self.scheduler.timerIntr(self.processor.getTicks())

                timerEvent = TimerEvent(event.getTime()+1)
                queue.addEvent(timerEvent)
                
            elif isinstance(event, TaskCreationEvent):
                task = event.getTask()
                
                print "Creating Task - ", task.getName()

                # inform scheduler of task creation
                self.scheduler.createTask(task)
                
            elif isinstance(event, TaskFinishEvent):
                task = event.getTask()
                
                print "Finishing Task - ", task.getName()

                # inform scheduler that task finished
                self.scheduler.finishTask(task)

                nTasks -= 1

                # all tasks finished
                if nTasks == 0:
                    return
                
            elif isinstance(event, IOStartEvent):
                task = event.getTask()
                
                premptRunningTask()
                
                print "IO Start - ", task.getName()

                task.setInIO(True)

                # inform scheduler that task is blocked
                self.scheduler.block(task)

                duration = event.getDuration()
                time = self.processor.getTicks() + duration

                ioCompleteEvent = IOCompleteEvent(time, task)
                queue.addEvent(ioCompleteEvent)
                
            elif isinstance(event, IOCompleteEvent):
                task = event.getTask()
                print "IO Complete - ", task.getName()

                task.setInIO(False)

                # inform scheduler that task is ready
                self.scheduler.unblock(task)
            else:
                print "Unkown event"
                sys.exit(1)

            task = self.processor.getRunningTask()
            assert not task.isInIO()

            # check if Start IO event must be generated
            if task is not None:
                nextEvent = queue.getMin()

                # there must always exist at least a timer interrupt
                assert nextEvent is not None

                window = nextEvent.getTime() - self.processor.getTime()
                
                if task.stillHasIO():
                    io = task.getNextIO()

                    relativeIOTime = io.getOffsetTime() - task.getUseCpuTime()

                    # IO will occur between the current time and the next event                    
                    if  window > relativeIOTime:
                        time = self.processor.getTime() + relativeIOTime
                        duration = io.getDuration()
                        ioStartEvent =  IOStartEvent(time, task, duration)
                        queue.addEvent(ioStartEvent)
                    # fi
                # fi
            # fi
        # while                    
# Simulator
