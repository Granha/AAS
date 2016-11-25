from scheduler.round_robin import RoundRobin

from simulator.simulator import Simulator
from simulator.workload_generator import WorkloadGenerator



if __name__ == '__main__':    
    wGen = WorkloadGenerator(num_jobs=40, rate_jobs=5, rate_io=2,
                             mean_job_time=1000, mean_io_time=3, sd_job_time=5,
                             sd_io_time=1, time_unit=1)

    scheduler = RoundRobin()
    
    simulator = Simulator(scheduler)

    workload = wGen.generateWorkload()

    simulator.setWorkload(workload)

    simulator.run()
