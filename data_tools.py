import pandas as pd

# https://pandas.pydata.org/docs/

# reading data from csv
equipment_df = pd.read_csv('data/equipment.csv') # equipment_type,prob_of_fail,min_hrs, max_hrs, fac1,fac2,fac3,fac4,fac5
facility_df = pd.read_csv('data/fac_detail.csv') # facility,latit,longit,max_occ
work_orders_df = pd.read_csv('data/work_orders.csv')  # order_id, facility, equipment_type,equipment_id,priority, completion_time,submission_time
workers_df = pd.read_csv('data/workers.csv')  # name,equipment_cert,shift,latit,longit

# cleaning
workers_df['equipment_cert'] = workers_df['equipment_cert'].str.lower()
work_orders_df['submission_time'] = pd.to_datetime(work_orders_df['submission_time'])

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
    matches = workers_df['equipment_cert'].str.contains(machine)
    names = workers_df.loc[matches, 'name']
    return names






