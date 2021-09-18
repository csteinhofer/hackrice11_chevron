import load_data as data
equipment = data.equipment_dict()
workers = dict([])

""" 
Goes through a dictionary of equipment and returns a list of equipment with the 
specified priority number.
"""
def getPriority(equipment, num):
    priority = []
    for (machine in equipment):
        # if the priority number matched at the dictionary matches the specified one,
        # add the equipment to the priority list
        if (equipment.get(machine) == num):
            priority.add(equipment)
    return priority

"""
Goes through a dictionary of equipment and workers, and matches workers to equipment.
Bases the matching off of certifications and completion times.
"""
def matchWorkers(equipment, workers):
    matches = dict([])
    for (machine in equipment):
        # first determining who can fix the machine
        if (workers.get(machine.get(certification)) > 1):
            times = []
            # go through workers and see who has the shortest time left
            for (worker in workers):
                times.add(worker.timeleft() + worker.distance())
            lowest_time = times.min()
            # we have a dictionary of matches, but it stores a list of the machines the worker is assigned to
            matches[workers[times.index(lowest_time)]].add(machine)
            # we need to update the time it will take for the worker to complete their tasks based on the new assignment
            workers[times.index(lowest_time)] = workers[times.index(lowest_time)] + worker.distance() + machine.time_to_fix()
    return matches

"""
Will take a list of equipment to be fixed and create a schedule of work orders.
"""
def workOrder(equipment):
    # first determining highest priority work orders
    for (i in [5, 4, 3, 2, 1]):
        if (getPriority(equipment, i).length > 1):
            # this should be a dictionary of workers as keys and a list of machines to fix as values
            workers = matchWorkers(getPriority(equipment, i), workers)

    return workers
