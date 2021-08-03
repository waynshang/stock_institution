from sqlalchemy import Column, Integer, String, Numeric, BigInteger, Date, DateTime
from sqlalchemy.orm import declarative_base
import re
from datetime import date, datetime
from model.stock_institutions_log import StockInstitutionsLog
from utils import update_table_and_insert_log
Base = declarative_base()
MappingTable = {
  "Institutional Ownership": "institutional_ownership",
  "Total Shares Outstanding (millions)":"total_share_out_standing",
  "Total Value of Holdings (millions)":"total_value_of_holdings"
}
EXCLUDE_COLUMNS = ['symbol', 'date', 'updated_at']
LOG_EXCLUDE_COLUMNS = StockInstitutionsLog.EXCLUDE_COLUMNS
class StockInstitution(Base):
  __tablename__ = 'stock_institutions'
  symbol = Column(String, primary_key=True)
  institutional_ownership = Column(Numeric)
  total_share_out_standing = Column(BigInteger)
  total_value_of_holdings = Column(BigInteger)
  date = Column(Date)
  # created_at = Column(DateTime)
  updated_at = Column(DateTime)

  def update(self, kwargs):
    for key, value in kwargs.items():
        if hasattr(self, key):
            setattr(self, key, value)
  
  @staticmethod
  def fetch_institution_data_from_api_response(response):
    ownershipSummaries = response["ownershipSummary"].values()
    result = {}
    for ownershipSummary in ownershipSummaries or []:
      result = StockInstitution.mapping_response_data_to_sql_column(ownershipSummary, result)
    return result
  
  def mapping_response_data_to_sql_column(ownershipSummary, result):
    if ownershipSummary is None: return result
    value = float(ownershipSummary["value"].replace("%","").replace(",","").replace("$",""))
    label = MappingTable[ownershipSummary["label"]]
    if label: result[label] = value
    return result
  
  def insert_or_update(session, institution_date, symbol):
    session, date = update_table_and_insert_log(session, institution_date, symbol, StockInstitution, 
    StockInstitutionsLog)
    return session, date

  def get_data_by_column(session, value, column):
    return session.query(StockInstitution).filter(getattr(StockInstitution, column) == value).first()
 
  
  def __repr__(self):
    return "<StockInstitution(symbol='%s', institutional_ownership='%s', total_share_out_standing='%s', total_value_of_holdings='%s', date='%s')>" % (
    self.symbol, self.institutional_ownership, self.total_share_out_standing, self.total_value_of_holdings, self.date)