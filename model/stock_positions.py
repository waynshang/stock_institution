from sqlalchemy import Column, Integer, String, Numeric, BigInteger, Date, DateTime
from sqlalchemy.orm import declarative_base
import re
from itertools import repeat
from datetime import date, datetime
from model.stock_positions_log import StockPositionsLog, EXCLUDE_COLUMNS as LOG_EXCLUDE_COLUMNS
from utils import model2dict, insert_or_update as utils_insert_or_update

Base = declarative_base()
MappingTable = {
  "Increased Positions": "increased_positions",
  "Decreased Positions":"decreased_positions",
  "Held Positions":"held_positions",
  "Total Institutional Shares":"total_institutional",
  "New Positions": "new_positions",
  "Sold Out Positions": "sold_out_positions"
}
EXCLUDE_COLUMNS = ['symbol', 'date', 'updated_at']
class StockPosition(Base):
  __tablename__ = 'stock_positions'
  symbol = Column(String, primary_key=True)
  increased_positions_holders = Column(BigInteger)
  increased_positions_shares = Column(BigInteger)
  decreased_positions_holders = Column(BigInteger)
  decreased_positions_shares = Column(BigInteger)
  held_positions_holders = Column(BigInteger)
  held_positions_shares = Column(BigInteger)
  total_institutional_holders = Column(BigInteger)
  total_institutional_shares = Column(BigInteger)
  new_positions_holders = Column(BigInteger)
  new_positions_shares = Column(BigInteger)
  sold_out_positions_holders = Column(BigInteger)
  sold_out_positions_shares = Column(BigInteger)
  date = Column(Date)
  # created_at = Column(DateTime)
  updated_at = Column(DateTime)
  


  def handle_position_data(data, type):
    result = {}
    for d in data or []:
      result = StockPosition.mapping_response_data_to_sql_column(d, type, result)
    return result
  
  def mapping_response_data_to_sql_column(data, type, result):
    if data is None: return result
    value = int(data[type].replace("%","").replace(",","").replace("$",""))
    label = MappingTable[data["positions"]]
    if label:
      label = label + "_" + type
      result[label] = value
    return result

  def insert_or_update(session, position_data, symbol):
    position_results = session.query(StockPosition).filter(StockPosition.symbol == symbol)#.first()
    session = utils_insert_or_update(session, position_data, symbol, StockPosition, 
    StockPositionsLog, position_results, EXCLUDE_COLUMNS, LOG_EXCLUDE_COLUMNS)
    return session
