import mysql.connector
import json
from model.error_log import ErrorLog
# from utils import getLogger
# DEBUG = getLogger()
class GainLossLog():

  @staticmethod
  def insert_to_db(cursor, db, insert_data, file_name):
    try:

      sqlStuff = "INSERT INTO gain_loss_log (`symbol`, `description`, `quantity`, `days_held`, `date_required`, `date_sold`, `sales_amount`, `cost`, `gain_loss`, `file_name`) VALUES (%s, %s, %s, %s, %s, %s , %s, %s, %s, %s)"
      cursor.executemany(sqlStuff, [insert_data]) 
      db.commit()
      DEBUG.debug("inert success: {}".format(insert_data))
      return cursor
    except mysql.connector.Error as error:
      db.rollback()
      DEBUG.error("Failed to insert into MySQL table {}".format(error))
      DEBUG.error("insert_data: {}".format(insert_data))
      ErrorLog.insert_to_db(error, cursor, db, insert_data, file_name)

