# Workload Metric Computator from Estimates
class Metric:

    # interactiveness estimate
    @staticmethod
    def interacMetric(tasks):
        
        interact = [ task.getAvgBlocking() for task in tasks ]

        return interact
    # interacMetric


    # minimization objective function
    # input parameters tasks: this is the list of tasks, currentProcessorTime: this is the CPU time field of a processor object
    @staticmethod
    def objFunction(tasks, currentProcessorTime):
        interact = Metric.interacMetric(tasks)
        
        # processing estimate
        proc = [ 1-v for v in interact ]

        partI = [ interact[i]*((tasks[i].getAvgReadyWait())**4) \
                  for i in xrange(len(interact)) \
                  if interact[i] >= 0.5 ]
        partC = [ tasks[i].getUsedCpuTime()/(currentProcessorTime - tasks[i].getCreationTime()) \
                       for i in xrange(len(proc)) \
                       if proc[i] > 0.5]
        objectivevalue = sum( partI) + sum(partC)
        
        return objectivevalue
    # objFunction

# Metric
