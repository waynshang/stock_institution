import mysql.connector
from config import secret
import sqlalchemy

def connect(way, database, server_name):
  try:
    host = secret[server_name]['mysql']['host']
    port = secret[server_name]['mysql']['port']
    username = secret[server_name]['mysql']['username']
    password = secret[server_name]['mysql']['password']
    if way == 'mysql':
      db = mysql.connector.connect(
        host = host,
        user = username,
        password = password,
        database = database
        # auth_plugin='mysql_native_password'
        )
      return db
    elif way == 'sqlalchemy':
      url = "mysql://{}:{}@{}/{}".format(username,password,host,database)
      print(url)
      engine = sqlalchemy.create_engine(url, echo=False)
      return engine
  except mysql.connector.Error as error:
    print(" {}".format(error))
  return None
