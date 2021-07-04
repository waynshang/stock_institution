from .model_util import *
from .mmpro_util import *
import csv
import os
import glob

def get_certain_format_files_from_path(path = './', format='csv'):
  result = glob.glob('{}*.{}'.format(path, format))
  print("get_certain_format_files_from_path")
  print(result)
  return result

