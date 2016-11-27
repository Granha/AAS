from processor import Processor

# Events
from event_queue import EventQueue
from task_creation_event import TaskCreationEvent
from task_finish_event import TaskFinishEvent
from timer_event import TimerEvent
from io_start_event import IOStartEvent
from io_complete_event import IOCompleteEvent

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

    # Generate Events that are not triggered by
    # the processing of other events, namely
    # IO Start and Task Finish. The logic for
    # these event is more sophisticated.
    def genNonTriggeredEvents(self, queue):
        task = self.processor.getRunningTask()
        assert not task.isInIO()

        if task is None or task.isIdleTask():
            return        
        
        nextEvent = queue.getMin()

        # there must always exist at least a timer interrupt
        assert nextEvent is not None
        window = nextEvent.getTime() - self.processor.getTime()
                
        if task.stillHasIO():
            io = task.getNextIO()

            relativeIOTime = io.getOffsetTime() - task.getUsedCpuTime()
            assert relativeIOTime >= 0

            # IO will occur between the current time and the next event                    
            if  window > relativeIOTime:
                task.popNextIO()
                time = self.processor.getTime() + relativeIOTime
                duration = io.getDuration()
                ioStartEvent =  IOStartEvent(time, task, duration)
                queue.addEvent(ioStartEvent)
            # fi
        else:
            relativeFinishTime = task.getTotalCpuTime() - task.getUsedCpuTime()
            assert relativeFinishTime >= 0
            
            if window > relativeFinishTime:
                time = self.processor.getTime() + relativeFinishTime
                taskFinishEvent =  TaskFinishEvent(time, task)
                queue.addEvent(taskFinishEvent)
            # fi
        # fi
    # genEvent
    
    def run(self):                
        # initialize event queue with creation
        initialEvents = self.workload.getInitialEvents()
        queue = EventQueue(initialEvents)

        # number of alive tasks
        nTasks = queue.getSize()

        # there are no tasks
        if nTasks == 0:
            return
        
        # first timer event
        timerEvent = TimerEvent(0)
        queue.addEvent(timerEvent)

        self.scheduler.start()

        # Main Loop
        while not queue.isEmpty():
            event = queue.extractMin()
            
            # time can be an arbitrary real number
            self.processor.setTime(event.getTime())
            self.processor.updateRunningTask()
            
            if isinstance(event, TimerEvent):
                print "Timer Event [Tick=%d]" % event.getTime()

                # tick is only integer
                self.processor.setTicks(event.getTime())

                # inform scheduler of timer interrupt
                self.scheduler.timerIntr(self.processor.getTicks())

                timerEvent = TimerEvent(event.getTime()+1)
                queue.addEvent(timerEvent)
                
            elif isinstance(event, TaskCreationEvent):
                task = event.getTask()
                
                print "Creating Task: ", task.getName()

                # inform scheduler of task creation
                self.scheduler.createTask(task)
                
            elif isinstance(event, TaskFinishEvent):
                task = event.getTask()

                self.processor.premptRunningTask()                
                
                print "Finishing Task: ", task.getName()
                print "Used CPU Time: ", task.getUsedCpuTime()
                print "Total CPU Time: ", task.getTotalCpuTime()

                # inform scheduler that task finished
                self.scheduler.finishTask(task)

                # TODO: fix finishing bug
                if len(self.scheduler.getAllTaks()) == 0:
                    return                
                
            elif isinstance(event, IOStartEvent):
                task = event.getTask()
                runningTask = self.processor.getRunningTask()

                assert task is runningTask
                
                self.processor.premptRunningTask()
                
                print "IO Start: ", task.getName()
                print "IO Durration: ", event.getDuration()
                print "Used CPU time: ", task.getUsedCpuTime()

                task.setInIO(True)

                # inform scheduler that task is blocked
                self.scheduler.block(task)

                duration = event.getDuration()
                time = self.processor.getTime() + duration

                ioCompleteEvent = IOCompleteEvent(time, task)
                queue.addEvent(ioCompleteEvent)
                
            elif isinstance(event, IOCompleteEvent):
                task = event.getTask()
                print "IO Complete: ", task.getName()

                # inform scheduler that task is ready
                self.scheduler.unblock(task)
            else:
                print "Unkown event"
                sys.exit(1)

            self.genNonTriggeredEvents(queue)

            print "Running Task", self.processor.getRunningTask().getName()
        # while

# Simulator
