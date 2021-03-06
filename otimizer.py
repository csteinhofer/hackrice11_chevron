# import required libraries & scripts
import data_tools, demo_driver


def get_eligible_workers(equipment_type):
    shift = demo_driver.get_current_shift()
    elig_worker = data_tools.get_cert_workers([equipment_type])
    for worker in elig_worker:
        current_worker_shift = data_tools.get_shift(worker)
        res = []
        if current_worker_shift == shift:
            res.append(worker)
    return res


# {'order_id': 1001, 'facility': 'Fac1', ' equipment_type': 'Pump', 'equipment_id': 'P032', 'priority': 5,
# 'completion_time': 3, 'submission_time': Timestamp('2018-09-14 22:12:00')},
def assign_work(workorder):
    """
    takes single work order dictionary and assigns it to a worker's queue
    queries worker, facility, and equipment tables to place in most optimal position
    :param workorder:
    :return: none -- updates data tables to reflect worker assignments
    """

    # get cert techs
    elig_workers = get_eligible_workers(workorder['equipment_type'])

    # get facility location and calculate travel time and note if full
    wo_fac = data_tools.get_facility_detail(workorder['facility'])
    gmaps_tools.get_drive_time(wo_fac['latit'], wo_fac['longit'])

    # need to figure out how to store current time left of job -- feature in workers?

    # check priority
    #


def on_submission(workorder):
    """
    accepts a dictionary containing all information about a work order and processes it
    if multiple work orders are submitted as a list it will process them in arbitrary order
    :param workorder:
    :return:
    """
    pass
