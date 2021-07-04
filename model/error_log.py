import mysql.connector

class ErrorLog:
  @staticmethod
  def insert_to_db(error, cursor, db, data , file_name):  
    try:
      sqlStuff = "INSERT INTO error_log (`error`, `data`, `file_name`) VALUES (%s, %s, %s)"
      cursor.executemany(sqlStuff, [(str(error), str(data), file_name)])
      db.commit()
    except mysql.connector.Error as error:
      print("handle_error failed {}".format(error))
      # handle_error(error, cursor, db,row,file_name)
