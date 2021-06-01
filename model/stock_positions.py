from sqlalchemy import Column, Integer, String, Numeric, BigInteger, Date, DateTime
from sqlalchemy.orm import declarative_base
import re
from itertools import repeat
from datetime import date, datetime
from model.stock_positions_log import StockPositionsLog, EXCLUDE_COLUMNS as LOG_EXCLUDE_COLUMNS
from utils import model2dict

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
    if position_data:
        position_data["symbol"] = symbol
        position_data["date"] = date.today()
        # session.add(StockPosition(**position_data))
        # session.execute(StockPosition.insert(), [position_data])
        if position_results.first():
            position_result = position_results.first()
            compared_columns = list(set(position_data.keys())-set(EXCLUDE_COLUMNS))
            # filter_result = list(filter(lambda i: float(vars(position_result)[i]) != float(position_data[i]), compared_columns))
            filter_result = []
            for column in compared_columns:
              print(column)
              print(float(vars(position_result)[column]))
              print(float(position_data[column]))
              if float(vars(position_result)[column]) != float(position_data[column]): filter_result.append(column)
            print(filter_result)
            if len(filter_result) >0: 
              position_data["updated_at"] = datetime.now()
              position_results.update(position_data)
              log_data = model2dict(StockPosition, position_result, LOG_EXCLUDE_COLUMNS)
              session.add(StockPositionsLog(**log_data))

        else:
            position_data["updated_at"] = datetime.now()
            session.add(StockPosition(**position_data))
            # session.add(StockPosition(**position_data))
    return session
