from db.db_connector import MysqlConnection;
import mysql.connector
from utils import getLogger
DEBUG = getLogger()
class MysqlConnector(MysqlConnection):  

  def __init__(self, database, server_name):
    super().__init__(database, server_name)

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
      DEBUG.error(" {}".format(error))
    return None
