import urllib3
from db.sql_alchemy import SqlAlchemyConnector
from request import get_nasdaq_institution_from_api
from sqlalchemy.orm import Session
from model.stock_institutions import StockInstitution
from model.stock_positions import StockPosition
from datetime import date
from sqlalchemy import select


def main(params):
    response = get_api_response(params["stock"])
    print(response)
    if response : 
        institution_date, position_date = fetch_institution_and_position_data_from_api_response(response) 
        if institution_date or position_date : insert_or_update_db(institution_date, position_date, params["stock"])
    

def get_api_response(stock):
    # TODO implement
    response = get_nasdaq_institution_from_api(stock)
    if response and response["data"] : return response["data"]
    return None

def fetch_institution_and_position_data_from_api_response(response):
    print("fetch_institution_and_position_data_from_api_response")
    # {'institutional_ownership': 57.56, 'total_share_out_standing': 16688.0, 'total_value_of_holdings': 1364155.0}
    # {'increased_positions_shares': 162714490, 'decreased_positions_shares': 376214279, 
    # 'held_positions_shares': 9066444362, 'total_institutional_shares': 9605373131, 
    # 'new_positions_shares': 14960170, 'sold_out_positions_shares': 16852823, 
    # 'increased_positions_holders': 1670, 'decreased_positions_holders': 2059, 
    # 'held_positions_holders': 202, 'total_institutional_holders': 3931, 
    # 'new_positions_holders': 159, 'sold_out_positions_holders': 109}
    institution_date = StockInstitution.fetch_institution_data_from_api_response(response)
    position_date = StockPosition.fetch_position_data_from_api_response(response)

    return institution_date, position_date    

def insert_or_update_db(institution_date, position_date, symbol):
    connector = SqlAlchemyConnector('stock', 'local')
    engine = connector.connect()
    # create session and add objects
    with Session(engine) as session:
        # result = session.execute(select(StockInstitution))
        print("======StockInstitution====")
        session = StockInstitution.insert_or_update(session, institution_date, symbol)
        print("======StockPosition====")
        session = StockPosition.insert_or_update(session, position_date, symbol)
        session.commit()

if __name__ == '__main__':
    try:
        lt = ["AAPL", "AMZN", "AMD", "AA", "DIS", "F", "FB", "GOOG", "GS", "MSFT", "NFLX", "NVDA", "NUE","SQ", "SLB","SHOP", "TDOC", "TSLA", "TSM", "U", "UPST", "X"]
        lt = ["AAPL", "FB"]
        # lt = ["NUE"]
        for symbol in lt:
            print("==========symbol: {}".format(symbol))
            main({"stock": symbol})
    except KeyboardInterrupt:
        exit()