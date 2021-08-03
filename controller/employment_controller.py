import urllib3
import os
import sys
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
from request import get_employment_data
from datetime import date
from utils import get_label_data, getLogger
DEBUG = getLogger()
def main(label, commencement_date, end_date):
  result = get_employment_data()
  try:
    value_within_date = get_label_data(result, label, commencement_date, end_date)
  except Exception as error:
    DEBUG.error("======Error======")
    if 'msg' in result: DEBUG.info(result['msg'])
    DEBUG.error("{}".format(error))
    return {}

  DEBUG.info(value_within_date)
  total = 0
  for value in value_within_date.values():
    total += value
  DEBUG.info(total)


if __name__ == '__main__':
    try:
      commencement_date = '2020-03-01'
      end_date = '2021-05-01'
      label = "c:36"
      main(label, commencement_date, end_date)
    except KeyboardInterrupt:
        exit()