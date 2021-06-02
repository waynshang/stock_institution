from sqlalchemy import Column, Integer, String, Numeric, BigInteger, Date, DateTime
from sqlalchemy.orm import declarative_base
import re
from datetime import date, datetime
from model.stock_institutions_log import StockInstitutionsLog, EXCLUDE_COLUMNS as LOG_EXCLUDE_COLUMNS
from utils import model2dict, insert_or_update as utils_insert_or_update
Base = declarative_base()
MappingTable = {
  "Institutional Ownership": "institutional_ownership",
  "Total Shares Outstanding (millions)":"total_share_out_standing",
  "Total Value of Holdings (millions)":"total_value_of_holdings"
}
EXCLUDE_COLUMNS = ['symbol', 'date', 'updated_at']
class StockInstitution(Base):
  __tablename__ = 'stock_institutions'
  symbol = Column(String, primary_key=True)
  institutional_ownership = Column(Numeric)
  total_share_out_standing = Column(BigInteger)
  total_value_of_holdings = Column(BigInteger)
  date = Column(Date)
  # created_at = Column(DateTime)
  updated_at = Column(DateTime)

  def handle_institution_data(data):
    result = {}
    for d in data or []:
      result = StockInstitution.mapping_response_data_to_sql_column(d, result)
    return result
  
  def mapping_response_data_to_sql_column(data, result):
    if data is None: return result
    value = float(data["value"].replace("%","").replace(",","").replace("$",""))
    label = MappingTable[data["label"]]
    if label: result[label] = value
    return result
  
  def insert_or_update(session, institution_date, symbol):
    institution_results = session.query(StockInstitution).filter(StockInstitution.symbol == symbol)#.first()
    session = utils_insert_or_update(session, institution_date, symbol, StockInstitution, 
    StockInstitutionsLog, institution_results, EXCLUDE_COLUMNS, LOG_EXCLUDE_COLUMNS)
    return session
  


    

  def __repr__(self):
    return "<StockInstitution(symbol='%s', institutional_ownership='%s', total_share_out_standing='%s', total_value_of_holdings='%s', date='%s')>" % (
    self.symbol, self.institutional_ownership, self.total_share_out_standing, self.total_value_of_holdings, self.date)