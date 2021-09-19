import pandas as pd

# https://pandas.pydata.org/docs/

# reading data from csv
equipment_df = pd.read_csv(
    'data/equipment.csv')  # equipment_type,prob_of_fail,min_hrs, max_hrs, fac1,fac2,fac3,fac4,fac5
facility_df = pd.read_csv('data/fac_detail.csv')  # facility,latit,longit,max_occ
work_orders_df = pd.read_csv(
    'data/work_orders.csv')  # order_id, facility,equipment_type,equipment_id,priority, completion_time,submission_time
workers_df = pd.read_csv('data/workers.csv')  # name,equipment_cert,shift,latit,longit

# cleaning
# setting equipment type to lower for matching
workers_df['equipment_cert'] = workers_df['equipment_cert'].str.lower()
workers_df['name'] = workers_df['name'].str.lower()
workers_df['shift'] = workers_df['shift'].str.lower()
work_orders_df['equipment_type'] = work_orders_df['equipment_type'].str.lower()
work_orders_df['facility'] = work_orders_df['facility'].str.lower()

# creates datetime objects for submission time in work order table
work_orders_df['submission_time'] = pd.to_datetime(work_orders_df['submission_time'])

# creating new features for live updating
facility_df['c_occ'] = 0


def equipment_dict():
    """

    :return: returns dictionary representation of equipment data
    """
    return equipment_df.to_dict(orient='records')


def facility_dict():
    """

    :return: returns dictionary representation of facility data
    """
    return facility_df.to_dict(orient='records')


# wrangling data
def get_cert_workers(machine):
    """
    given a type of machine return a list of workers who are certified to work with it
    :param machine: str
    :return: list of worker names str
    """
    # should be implemented with sql but using pandas/csv for now
    # SELECT w.name FROM workers w WHERE equipment_cert = machine
    matches = workers_df['equipment_cert'].str.match(machine)
    names = workers_df.loc[matches, 'name']
    return names


def get_shift(worker):
    """
    :param worker: name str of worker
    :return: worker's shift (morning or evening)
    """
    name = workers_df.loc[workers_df['name'] == worker, 'shift']
    return name[0]


def get_facility_detail(facility):
    """
    :param facility: facility name
    :return: dictionary of current facility details
    """
    fac_ind = {'fac1': 0, 'fac2': 1, 'fac3': 2, 'fac4': 3, 'fac5': 4}
    return facility_df.iloc[fac_ind[facility], 1:5].to_dict()

def move_worker(name, facility):
    """
    update worker location based on facility
    :param name: worker name str
    :param facility: facility name str
    :return: none -- updates data to reflect change
    """
    pass


def get_work_order(timestamp):
    """
    returns a dictionary representation of the work order(s) that was/were submitted in the hour of timestamp
    returns list of dictionaries if multiple
    :param timestamp:
    :return:
    """

    work_orders_df.iloc[0:2].to_dict(orient='records')
    pass
