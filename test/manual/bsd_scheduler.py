from scheduler.bsd_scheduler import BSDScheduler

from simulator.simulator import Simulator
from simulator.workload_generator import WorkloadGenerator


if __name__ == '__main__':    
    scheduler = BSDScheduler(enableEuler=False)
    
    simulator = Simulator(scheduler)

    workload = WorkloadGenerator.dummyGen()

    simulator.setWorkload(workload)

    simulator.run()
