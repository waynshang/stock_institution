
import csv
import os
import glob
# import mysql.connector
from datetime import datetime
import json 
from db.mysql_connector import MysqlConnector
import mysql.connector




          
def import_data(file_name = None):
  try:
    path = "/"
    extension = 'csv'
    # os.chdir(path)
    result = glob.glob('*.{}'.format(extension))
    print(result)
    connector = MysqlConnector('stock', 'local')
    db = connector.connect()
    cursor=db.cursor()
    for file_name in result:
      print("----------------{}---------------".format(file_name))
      with open(file_name, newline='') as csvfile:
        # read CSV content
        rows = csv.reader(csvfile)
        next(rows) # next first row
        # for loop
        find = "SELECT * from gain_loss_log where file_name = %s"
        cursor.execute(find, (file_name, ))
        find_result = cursor.fetchall()
        # print(cursor.fetchall())
        if not find_result:
          for row in rows:
            new_row = list(map(mapfunction, enumerate(row)))
            new_row.append(file_name)
            print("---new_row----")
            print(new_row)
            insert_data = [tuple(new_row)]
          
            # row.append(file_name)
            
            print("ready to insert")
            try: 
              if row[0]:
                sqlStuff = "INSERT INTO gain_loss_log (`symbol`, `desciption`, `quantity`, `days_held`, `date_required`, `date_sold`, `sales_amount`, `cost`, `gain_loss`, `file_name`) VALUES (%s, %s, %s, %s, %s, %s , %s, %s, %s, %s)"
                cursor.executemany(sqlStuff, insert_data) #[(row[0],row[1],row[2],row[3],row[4],row[5],row[6].replace('$', ''),row[7].replace('$', '').replace(',', ''),row[8].replace('$', '').replace(',', ''),row[9])])
                db.commit()
                print(cursor.rowcount, "Record inserted successfully into stock table")
            except mysql.connector.Error as error:
              print("Failed to insert into MySQL table {}".format(error))
              handle_error(error, cursor, db, row, file_name)
        else:
          pass
          # print("File already input {}".format(find_result))
  except mysql.connector.Error as error:
    print("{}".format(error))

def mapfunction(data):
  i = list(data)[0]
  el = list(data)[1]
  if i in (4,5):
    return datetime.strptime(el, "%m/%d/%Y")
  elif i in (6,7,8):
    return el.replace('$', '').replace(',', '')
  else:
    return el


def handle_error(error, cursor, db, data , file_name):
  try:
    sqlStuff = "INSERT INTO error_log (`error`, `data`, `file_name`) VALUES (%s, %s, %s)"
    cursor.executemany(sqlStuff, [(str(error), str(json.dumps(data)), file_name)])
    db.commit()
  except mysql.connector.Error as error:
    print("handle_error failed {}".format(error))
    # handle_error(error, cursor, db,row,file_name)

if __name__ == '__main__':
    try:
        import_data()
    except KeyboardInterrupt:
        exit()