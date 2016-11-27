from scheduler.round_robin import RoundRobin

from simulator.simulator import Simulator
from simulator.workload_generator import WorkloadGenerator


import copy


if __name__ == '__main__':    
    wGen = WorkloadGenerator(num_jobs=1000, rate_jobs=5, rate_io=0.3,
                             mean_job_time=100, mean_io_time=3,
                             sd_job_time=5, sd_io_time=1, time_unit=1)

    ##############################
    #   Simulate with Euler
    ##############################
    scheduler = RoundRobin(enableEuler=True)    
    simulator = Simulator(scheduler)
    workload1 = wGen.generateWorkload()
    
    workload2 = copy.deepcopy(workload1)
    simulator.setWorkload(workload1)
    simulator.run()

    ##############################
    #   Simulate without Euler
    ##############################    
    scheduler = RoundRobin(enableEuler=False)
    
    simulator = Simulator(scheduler)

    simulator.setWorkload(workload2)
    simulator.run()
    
