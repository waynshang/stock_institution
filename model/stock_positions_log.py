from sqlalchemy import Column, Integer, String, Numeric, BigInteger, Date, DateTime
from sqlalchemy.orm import declarative_base
import re
from datetime import date, datetime
from utils import getLogger
from . import stock_positions

DEBUG = getLogger()
Base = declarative_base()
MappingTable = {
  "Increased Positions": "increased_positions",
  "Decreased Positions":"decreased_positions",
  "Held Positions":"held_positions",
  "Total Institutional Shares":"total_institutional",
  "New Positions": "new_positions",
  "Sold Out Positions": "sold_out_positions"
}
class StockPositionsLog(Base):
  __tablename__ = 'stock_positions_log'
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
  EXCLUDE_COLUMNS = ['updated_at']




  def handle_position_data(data, type):
    result = {}
    StockPosition = stock_positions.StockPosition

    for d in data or []:
      result = stock_positions.StockPosition.mapping_response_data_to_sql_column(d, type, result)
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
    StockPosition = stock_positions.StockPosition

    position_results = session.query(StockPosition).filter(StockPosition.symbol == symbol)#.first()
    if position_data:
        position_data["symbol"] = symbol
        position_data["date"] = date.today()
        # session.add(StockPosition(**position_data))
        # session.execute(StockPosition.insert(), [position_data])
        if position_results.first():
            position_result = position_results.first()
            compared_columns = list(set(position_data.keys())-set(stock_positions.EXCLUDE_COLUMNS))
            filter_result = list(filter(lambda i: float(vars(position_result)[i]) != float(position_data[i]), compared_columns))
            DEBUG.info(filter_result)
            if len(filter_result) >0: 
              position_data["updated_at"] = datetime.now()
              position_results.update(position_data)
        else:
            session.add(stock_positions(**position_data))
            # session.add(StockPosition(**position_data))
    return session

  def insert_data_difference_to_log(session, data_from_api, old_data):
    exclude_columns = stock_positions.EXCLUDE_COLUMNS
    compared_columns = list(set(data_from_api.keys())-set(exclude_columns))
    for column in compared_columns:
      old_data[column] = float(data_from_api[column]) - float(old_data[column])
    session.add(StockPositionsLog(**old_data))
    return session
