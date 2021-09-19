import pandas as pd

start_dt = pd.to_datetime('2018-09-12 05:00:00')


def simulate_workday(start):
    """
    simulates a day of work with realtime schedule updates
    :param start: start timestamp @ 5am
    :return: none
    """
    dti = pd.date_range(start, periods=15, freq='H')
    for datetime in dti:
        pass


simulate_workday(start_dt)


def get_current_shift():
    return None