from db.mysql_connect import MysqlConnection;
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError

class SqlAlchemyConnector(MysqlConnection):

  def __init__(self, database, server_name):
    super().__init__(database, server_name)

  def connect(self):
    try:
      url = "mysql://{}:{}@{}/{}".format(self.username,self.password,self.host,self.database)
      engine = sqlalchemy.create_engine(url, echo=False)
      return engine
    except SQLAlchemyError as error:
      print(" {}".format(error))
    return None