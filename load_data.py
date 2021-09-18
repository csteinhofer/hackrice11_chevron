import pandas as pd

equipment_df = pd.read_csv('data/equipment.csv')
facility_df = pd.read_csv('data/fac_detail.csv')
work_orders_df = pd.read_csv('data/work_orders.csv')
workers_df = pd.read_csv('data/workers.csv')


def equipment_dict():
    """

    :return: returns dictionary representation of equipment data
    """
    return equipment_df.to_dict()

print(equipment_dict()
      )