from scheduler.round_robin import RoundRobin

from simulator.simulator import Simulator
from simulator.workload_generator import WorkloadGenerator



if __name__ == '__main__':    
    wGen = WorkloadGenerator(50,5, 2, 5, 2, 1, 1, 10000)
    scheduler = RoundRobin()
    
    simulator = Simulator(scheduler)

    workload = wGen.generateWorkload()

    simulator.setWorkload(workload)

    simulator.run()
