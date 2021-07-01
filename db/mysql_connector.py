from db.mysql_connect import MysqlConnect;
import mysql.connector

class MysqlConnector(MysqlConnect):  
  def __init__(self, database, server_name):
    super(MysqlConnect, self).__init__(database, server_name)

  def connect(self):
    try:
      db = mysql.connector.connect(
        host = self.host,
        user = self.username,
        password = self.password,
        database = self.database
      # auth_plugin='mysql_native_password'
      )
      return db
    except mysql.connector.Error as error:
      print(" {}".format(error))
    return None
