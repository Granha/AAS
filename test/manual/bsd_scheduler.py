from scheduler.bsd_scheduler import BSDScheduler
from scheduler.round_robin import RoundRobin

from simulator.simulator import Simulator
from simulator.workload_generator import WorkloadGenerator

import copy
import cProfile

DO_PROFILING = False

if __name__ == '__main__':
    ##############################
    #      Dummy Test
    ##############################    
    # scheduler = BSDScheduler(enableEuler=False)

    # simulator = Simulator(scheduler)            
                                                
    # workload = WorkloadGenerator.dummyGen()     
                                                
    # simulator.setWorkload(workload)             
                                                
    # simulator.run()                             
    
    
    wGen = WorkloadGenerator(num_jobs=2000, rate_jobs=5, rate_io=0.3,
                             mean_job_time=100, mean_io_time=3,
                             sd_job_time=5, sd_io_time=1, time_unit=1)

    ##############################
    #   Simulate with Euler
    ##############################
    scheduler = BSDScheduler(enableEuler=True)    
    simulator = Simulator(scheduler)
    workload1 = wGen.generateWorkload()
    
    workload2 = copy.deepcopy(workload1)
    workload3 = copy.deepcopy(workload1)
    workload4 = copy.deepcopy(workload1)

    simulator.setWorkload(workload1)    

    if DO_PROFILING:
        cProfile.run('simulator.run()')
    else:
        simulator.run()
        
    ##############################
    #   Simulate without Euler
    ##############################    
    scheduler = BSDScheduler(enableEuler=False)
    
    simulator = Simulator(scheduler)

    simulator.setWorkload(workload2)

    if DO_PROFILING:
        cProfile.run('simulator.run()')
    else:
        simulator.run()

    ##############################
    #   Simulate with Euler
    ##############################
    scheduler = RoundRobin(enableEuler=True)    
    simulator = Simulator(scheduler)
    workload1 = wGen.generateWorkload()
    
    workload2 = copy.deepcopy(workload1)
    simulator.setWorkload(workload3)
    simulator.run()

    ##############################
    #   Simulate without Euler
    ##############################    
    scheduler = RoundRobin(enableEuler=False)
    
    simulator = Simulator(scheduler)

    simulator.setWorkload(workload4)
    simulator.run()
