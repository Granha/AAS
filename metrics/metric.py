# Workload Metric Computator from Estimates
class Metric:

    # interactiveness estimate
    def interacMetric(self, tasks):
        
        interact = [ task.getAvgBlocking() for task in tasks ]

        return interact
    # interacMetric


    # minimization objective function
    def objFunction(self, tasks):
        interact = interacMetric(self, tasks)
        
        # processing estimate
        proc = [ 1-v for v in interact ]

        partI = [ interact[i]*((tasks[i].getAvgReadyWait())**4) \
                  for i in xrange(interact) \
                  if interact[i] >= 0.5 ]

        # TODO: also use processing estimate

        return partI
    # objFunction

# Metric
