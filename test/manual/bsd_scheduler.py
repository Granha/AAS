from scheduler.bsd_scheduler import BSDScheduler

from simulator.simulator import Simulator
from simulator.workload_generator import WorkloadGenerator


if __name__ == '__main__':
    
    wGen = WorkloadGenerator()
    scheduler = BSDScheduler()
    
    simulator = Simulator(scheduler)

    workload = wGen.dummyGen()

    simulator.setWorkload(workload)

    simulator.run()
