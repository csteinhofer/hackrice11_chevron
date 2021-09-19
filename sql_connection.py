#script to allow python to connect to the google cloud sql database
import os
import pymysql

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

def open_connection():
    """
    opens a connection to the database where work order information is stored
    :return: pymysql connection object
    """
    unix_soc = '/cloudsql/{}'.format(db_connection_name)
    try:
        if os.environ.get('GAE_EVN') == 'standard':
             conn = pymysql.connect(user=db_user, password=db_password,
                           unix_socket=unix_soc, db=db_name,
                           cursorclass=pymysql.cursors.DictCursor
                           )
    except pymysql.MySQLError as e:
        print(e)
    return conn





