from sqlalchemy import Column, Integer, String, Numeric, BigInteger, Date, DateTime
from sqlalchemy.orm import declarative_base
import re
from datetime import date, datetime
from model.stock_institutions_log import StockInstitutionsLog, EXCLUDE_COLUMNS as LOG_EXCLUDE_COLUMNS
from utils import model2dict
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
    if institution_date:
        institution_date["symbol"] = symbol
        institution_date["date"] = date.today()
        # session.add(StockInstitution(**institution_date))
        # session.execute(StockInstitution.insert(), [institution_date])
        filter_result = []
        if institution_results.first():
            institution_result = institution_results.first()
            compared_columns = list(set(institution_date.keys())-set(EXCLUDE_COLUMNS))
            for column in compared_columns:
              print(column)
              print(float(vars(institution_result)[column]))
              print(float(institution_date[column]))
              if float(vars(institution_result)[column]) != float(institution_date[column]): filter_result.append(column)
            # filter_result = list(filter(lambda i: float(vars(institution_result)[i]) != float(institution_date[i]), compared_columns))
            print("=====update {}======".format(len(filter_result) >0))
            print("filter_result: {}".format(filter_result))
            if len(filter_result) >0: 
              institution_date["updated_at"] = datetime.now()
              institution_results.update(institution_date)
              log_data = model2dict(StockInstitution, institution_result, LOG_EXCLUDE_COLUMNS)
              # print(log_data)
              session.add(StockInstitutionsLog(**log_data))
        else:
            institution_date["updated_at"] = datetime.now()
            session.add(StockInstitution(**institution_date))
            # session.add(StockInstitution(**institution_date))
    return session


    

  def __repr__(self):
    return "<StockInstitution(symbol='%s', institutional_ownership='%s', total_share_out_standing='%s', total_value_of_holdings='%s', date='%s')>" % (
    self.symbol, self.institutional_ownership, self.total_share_out_standing, self.total_value_of_holdings, self.date)