from simulator.workload_generator import WorkloadGenerator



if __name__ == '__main__':
    
    wGen = WorkloadGenerator(100, 5, 2, 5, 2, 1, 1, 1000)
    w = wGen.generateWorkload()
