

from datetime import datetime
from db.mysql_connector import MysqlConnector
from model.gain_loss_log import GainLossLog
import csv
import json
from utils import getLogger, get_certain_format_files_from_path, move_file
DEBUG = getLogger()

def import_data(file_name = None):
    csv_files = get_certain_format_files_from_path()
    connector = MysqlConnector('stock', 'local')
    db = connector.connect()
    cursor = db.cursor()
    for file_name in csv_files:
      file_name = file_name.split("/", 1).pop()
      DEBUG.info("----------------{}---------------".format(file_name))
      is_file_exist = check_file_exist(cursor, file_name)
      if is_file_exist: pass
      with open(file_name, newline='') as csvfile:
        # read CSV content
        rows = csv.reader(csvfile)
        next(rows) # next first row
        insert_data = format_gain_loss_log_data(rows, file_name)
        for row in insert_data:
          GainLossLog.insert_to_db(cursor, db, row, file_name)
        is_file_exist = check_file_exist(cursor, file_name)
        if is_file_exist: move_file(file_name, 'archive')
 
      

def check_file_exist(cursor, file_name):
  find = "SELECT * from gain_loss_log where file_name = %s"
  cursor.execute(find, (file_name, ))
  find_result = cursor.fetchall()
  return True if find_result else False

def mapfunction(data):
  i = list(data)[0]
  el = list(data)[1]
  if i in (4,5):
    return datetime.strptime(el, "%m/%d/%Y")
  elif i in (6,7,8):
    return el.replace('$', '').replace(',', '')
  else:
    return el

def format_gain_loss_log_data(rows, file_name):
  gain_loss_logs = []
  for row in rows:
    if row[0]:
      new_row = list(map(mapfunction, enumerate(row)))
      new_row.append(file_name)
    gain_loss_logs.append(tuple(new_row))
  return gain_loss_logs



if __name__ == '__main__':
    try:
      import_data()
    except KeyboardInterrupt:
        exit()