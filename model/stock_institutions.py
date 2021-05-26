from sqlalchemy import Column, Integer, String, Numeric, BigInteger, Date, DateTime
from sqlalchemy.orm import declarative_base
Base = declarative_base()
class StockInstitution(Base):
  __tablename__ = 'stock_institutions'
  symbol = Column(String, primary_key=True)
  institutional_ownership = Column(Numeric)
  total_share_out_standing = Column(BigInteger)
  total_value_of_holdings = Column(BigInteger)
  date = Column(Date)
  created_at = Column(DateTime)
  updated_at = Column(DateTime)

  def __repr__(self):
    return "<StockInstitution(symbol='%s', institutional_ownership='%s', total_share_out_standing='%s', total_value_of_holdings='%s', date='%s')>" % (
    self.symbol, self.institutional_ownership, self.total_share_out_standing, self.total_value_of_holdings, self.date)