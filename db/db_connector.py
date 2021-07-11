from config import secret
from utils import getLogger
DEBUG = getLogger()
class MysqlConnection:
  
  def __init__(self, database, server_name):
    self.host = secret[server_name]['mysql']['host']
    self.port = secret[server_name]['mysql']['port']
    self.username = secret[server_name]['mysql']['username']
    self.password = secret[server_name]['mysql']['password']
    self.database = database
