# Workload Metric Computator from Estimates
class Metric:


    def objFunction(self, tasks):
        # interactiveness estimate
        interact = [ task.getAvgBlocking() for task in tasks ]
        
        # processing estimate
        proc = [ 1-v for v in interact ]

        partI = [ interact[i]*((tasks[i].getAvgReadyWait())**4) \
                  for i in xrange(interact) \
                  if interact[i] >= 0.5 ]

        # TODO: use processing estimate

        return partI
    # objFunction

# Metric
