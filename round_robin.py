from scheduler.round_robin import RoundRobin

from simulator.simulator import Simulator
from simulator.workload_generator import WorkloadGenerator



if __name__ == '__main__':
    
    wGen = WorkloadGenerator()
    scheduler = RoundRobin()
    
    simulator = Simulator(scheduler)

    workload = wGen.dummyGen()

    simulator.setWorkload(workload)

    simulator.run()
