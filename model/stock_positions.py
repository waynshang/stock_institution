from sqlalchemy import Column, Integer, String, Numeric, BigInteger, Date, DateTime
from sqlalchemy.orm import declarative_base
import re

from model.stock_positions_log import StockPositionsLog, EXCLUDE_COLUMNS as LOG_EXCLUDE_COLUMNS
from utils import update_table_and_insert_log

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
POSITION_UNITS = ["shares", "holders"]

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


  def fetch_position_data_from_api_response(response):
    activePositions = response["activePositions"]["rows"]
    newSoldOutPositions = response["newSoldOutPositions"]["rows"]
    result = {}
    for unit in POSITION_UNITS:
      result = StockPosition.mapping_response_data_to_sql_column(activePositions, unit, result)
      result = StockPosition.mapping_response_data_to_sql_column(newSoldOutPositions, unit, result)
    return result
  
  def mapping_response_data_to_sql_column(data, type, result):
    for d in data:
      if d is None: next
      value = int(d[type].replace("%","").replace(",","").replace("$",""))
      label = MappingTable[d["positions"]]
      if label:
        label = label + "_" + type
        result[label] = value
    return result

  def insert_or_update(session, position_data, symbol):
    session = update_table_and_insert_log(session, position_data, symbol, StockPosition, StockPositionsLog)
    return session
    
  def get_data_by_column(session, value, column):
    return session.query(StockPosition).filter(StockPosition[column] == value).first()

