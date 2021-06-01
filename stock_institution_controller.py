import urllib3
import mysql_connect
from request import get_nasdaq_institution
from sqlalchemy.orm import Session
from model.stock_institutions import StockInstitution
from model.stock_positions import StockPosition
from datetime import date
from sqlalchemy import select


def main(params):
    response = get_response(params["stock"])
    print(response)
    if response and response["data"] : 
        institution_date, position_date = parse_response(response) 
        if institution_date or position_date : insert_or_update_db(institution_date, position_date, params["stock"])
    

def get_response(stock):
    # TODO implement
    response = get_nasdaq_institution(stock)
    return response
def parse_response(response):

    institution_date = StockInstitution.handle_institution_data(response["data"]["ownershipSummary"].values())
    active_position_share_date = StockPosition.handle_position_data(response["data"]["activePositions"]["rows"], "shares")
    active_position_holder_date = StockPosition.handle_position_data(response["data"]["activePositions"]["rows"], "holders")
    new_position_share_date = StockPosition.handle_position_data(response["data"]["newSoldOutPositions"]["rows"], "shares")
    new_position_holder_date = StockPosition.handle_position_data(response["data"]["newSoldOutPositions"]["rows"], "holders")
    # print(institution_date)
    # print(active_position_share_date)
    # print(active_position_holder_date)
    # print(new_position_share_date)
    # print(new_position_holder_date)
    return institution_date, {**active_position_share_date, **active_position_holder_date, **new_position_share_date, **new_position_holder_date}
    


def insert_or_update_db(institution_date, position_date, symbol):
    engine = mysql_connect.connect('sqlalchemy','stock', 'aws')
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
        # lt = ["AAPL", "AMZN", "AMD", "AA", "DIS", "F","FB", "GOOG", "GS", "MSFT", "NFLX", "NVDA", "SQ", "TDOC", "TSLA", "TSM", "U", "X"]
        lt = ["AAPL", "FB"]
        for symbol in lt:
            print("==========symbol: {}".format(symbol))
            main({"stock": symbol})
    except KeyboardInterrupt:
        exit()