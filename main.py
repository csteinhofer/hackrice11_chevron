# main.py
import datetime as datetime

import demo_driver
import data_tools
from flask import Flask, render_template
import sqlalchemy
import os
import datetime

app = Flask(__name__)


def init_connection_engine():
    db_config = {
        # [START cloud_sql_mysql_sqlalchemy_limit]
        # Pool size is the maximum number of permanent connections to keep.
        "pool_size": 5,
        # Temporarily exceeds the set pool_size if no connections are available.
        "max_overflow": 2,

        "pool_timeout": 30,  # 30 seconds
        # [END cloud_sql_mysql_sqlalchemy_timeout]
        "pool_recycle": 1800,  # 30 minutes
        # [END cloud_sql_mysql_sqlalchemy_lifetime]
    }

    if os.environ.get("DB_HOST"):
        return init_tcp_connection_engine(db_config)
    else:
        return init_unix_connection_engine(db_config)


def init_tcp_connection_engine(db_config):
    db_user = os.environ["DB_USER"]
    db_pass = os.environ["DB_PASS"]
    db_name = os.environ["DB_NAME"]
    db_host = os.environ["DB_HOST"]

    # Extract host and port from db_host
    host_args = db_host.split(":")
    db_hostname, db_port = host_args[0], int(host_args[1])

    pool = sqlalchemy.create_engine(
        # Equivalent URL:
        # mysql+pymysql://<db_user>:<db_pass>@<db_host>:<db_port>/<db_name>
        sqlalchemy.engine.url.URL.create(
            drivername="mysql+pymysql",
            username=db_user,  # e.g. "my-database-user"
            password=db_pass,  # e.g. "my-database-password"
            host=db_hostname,  # e.g. "127.0.0.1"
            port=db_port,  # e.g. 3306
            database=db_name,  # e.g. "my-database-name"
        ),
        **db_config
    )
    # [END cloud_sql_mysql_sqlalchemy_create_tcp]

    return pool


def init_unix_connection_engine(db_config):
    # [START cloud_sql_mysql_sqlalchemy_create_socket]
    # Remember - storing secrets in plaintext is potentially unsafe. Consider using
    # something like https://cloud.google.com/secret-manager/docs/overview to help keep
    # secrets secret.
    db_user = os.environ["DB_USER"]
    db_pass = os.environ["DB_PASS"]
    db_name = os.environ["DB_NAME"]
    db_socket_dir = os.environ.get("DB_SOCKET_DIR", "/cloudsql")
    cloud_sql_connection_name = os.environ["CLOUD_SQL_CONNECTION_NAME"]

    pool = sqlalchemy.create_engine(
        # Equivalent URL:
        # mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=<socket_path>/<cloud_sql_instance_name>
        sqlalchemy.engine.url.URL.create(
            drivername="mysql+pymysql",
            username=db_user,  # e.g. "my-database-user"
            password=db_pass,  # e.g. "my-database-password"
            database=db_name,  # e.g. "my-database-name"
            query={
                "unix_socket": "{}/{}".format(
                    db_socket_dir,  # e.g. "/cloudsql"
                    cloud_sql_connection_name)  # i.e "<PROJECT-NAME>:<INSTANCE-REGION>:<INSTANCE-NAME>"
            }
        ),
        **db_config
    )
    # [END cloud_sql_mysql_sqlalchemy_create_socket]

    return pool


@app.before_first_request
def test():
    global db
    db = init_connection_engine()
    with db.connect() as conn:
        data = conn.execute(
            "CREATE TABLE IF NOT EXISTS wo_queue"
            "(worker VARCHAR(50), order_id INT, priority INT, complete BOOLEAN DEFAULT 0, PRIMARY KEY (order_id))"
        )



@app.route('/', methods=['GET'])
def home():
    with db.connect() as conn:
        data = conn.execute(
            "SELECT * FROM workers"
        ).fetchall()
    print(data)
    return render_template('test.html', output_data=data)


@app.route('/test', methods=['GET'])
def test():
    facility = 'Fac1'
    with db.connect() as conn:
        q = sqlalchemy.text("SELECT * FROM facilities f WHERE f.name = :facility")
        data = conn.execute(q, facility=facility).fetchone()

    row2dict = {'latit':data[1], 'longit':data[2], 'max_occ': data[3], 'cur_occ':data[4]}
    print(str(row2dict))
    return row2dict


@app.route('/submit')
def submit():
    return render_template('submit.html')


@app.route('/demo', methods=['GET'])
def simulate_workday():
    """
    simulates a day of work with realtime schedule updates
    :return: none
    """

    def get_current_shift():
        return 'morning'

    def get_cert_workers(machine):
        """
        given a type of machine return a list of workers who are certified to work with it
        :param machine: str
        :return: list of worker names str
        """
        with db.connect() as conn:
            query = sqlalchemy.text("SELECT w.name FROM workers w WHERE :machine = w.equipment_cert")
            data = conn.execute(query, machine = machine)
        res = []
        for row in data:
            res.append(row)
        return res

    def get_shift(worker):
        """
        :param worker: name str of worker
        :return: worker's shift (morning or evening)
        """
        with db.connect() as conn:
            query = sqlalchemy.text("SELECT w.shift FROM workers w WHERE w.name = :worker")
            data = conn.execute(query, worker= worker).fetchone()
            print("get shift")
            print(data)
        return data

    def get_eligible_workers(equipment_type):
        shift = get_current_shift()
        elig_worker = get_cert_workers(equipment_type)
        for worker in elig_worker:
            res = []
            if get_shift(worker) == shift:
                res.append(worker)
        return res

    def get_facility_detail(facility):
        """
        :param facility: facility name
        :return: dictionary of current facility details
        """
        with db.connect() as conn:
            q = sqlalchemy.text("SELECT * FROM facilities f WHERE f.name = :facility")
            data = conn.execute(q, facility=facility).fetchone()
        row2dict = {'latit': data[1], 'longit': data[2], 'max_occ': data[3], 'cur_occ': data[4]}

        return row2dict

    def get_workorder(id):
        with db.connect() as conn:
            q = sqlalchemy.text("SELECT * FROM work_orders wo WHERE wo.order_id = :id")
            data = conn.execute(q, id=id).fetchone()
        row2dict = {'fac': data[1], 'equip': data[2], 'priority': data[4], 'est_time': data[5]}
        return row2dict


    def assign_work(workorder):
        """
        takes single work order dictionary and assigns it to a worker's queue
        queries worker, facility, and equipment tables to place in most optimal position
        :param workorder:
        :return: none -- updates data tables to reflect worker assignments
        """

        # get cert techs
        elig_workers = get_eligible_workers(workorder['equip'])
        with db.connect() as conn:
            q = sqlalchemy.text("INSERT INTO wo_queue VALUES ()")
            data = conn.execute(q, id=id).fetchone()

        # get facility location and calculate travel time and note if full
        #wo_fac = get_facility_detail(workorder['facility'])
        #gmaps_tools.get_drive_time(wo_fac['latit'], wo_fac['longit'])

        # check priority

    with db.connect() as conn:
        data = conn.execute(
            "SELECT order_id, submission FROM work_orders"
        ).fetchall()
        orders = []
        for row in data:
            orders.append((row[0], datetime.fromisoformat(row[1])))



    start = datetime.fromisoformat('2018-09-12T00:00:00')
    while start != datetime.fromisoformat('2018-09-13T00:00:00'):
        start = start+datetime.timedelta(minutes=1)
        result = next((i for i, v in enumerate(orders) if v[1] == start), None)
        result = orders[result][0]
        if result is not None:
            assign_work(get_workorder(result))



if __name__ == '__main__':
    app.run(debug=True)
