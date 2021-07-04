import mysql.connector
import json
from model.error_log import ErrorLog

class GainLossLog():

  @staticmethod
  def insert_to_db(cursor, db, insert_data, file_name):
    try:

      sqlStuff = "INSERT INTO gain_loss_log (`symbol`, `description`, `quantity`, `days_held`, `date_required`, `date_sold`, `sales_amount`, `cost`, `gain_loss`, `file_name`) VALUES (%s, %s, %s, %s, %s, %s , %s, %s, %s, %s)"
      cursor.executemany(sqlStuff, [insert_data]) 
      db.commit()
      return cursor
    except mysql.connector.Error as error:
      print("Failed to insert into MySQL table {}".format(error))
      ErrorLog.insert_to_db(error, cursor, db, insert_data, file_name)

