# WorkloadLearner probes the parameter space of
# a scheduler and learn dynamically the best
# parameters for a given workload.
class WorkloadLearner:    

    def __init__(self):
        # mapping from workload feature and scheduler
        # parameter to objective value
        self.mapping = []

    # Vary scheduler parameters
    # and store objective values
    def probeSchedule(self):

        return None

    # Use Neural Network (ELM) to learn
    # the best mapping from workload
    # features to parameter
    # (prior to this phase sufficient
    # data must have been collected)
    def learn(self):
        
        return None

# WorkloadLearner

