import urllib3
import mysql_connect
from request import get_nasdaq_institution
from sqlalchemy.orm import Session
from model.stock_institutions import StockInstitution
from sqlalchemy import select


def main(params):
    response = get_response(params["stock"])
    print(response)
    if response and response["data"] : parse_response(response) 
    insert_db(response)
    

def get_response(stock):
    # TODO implement
    response = get_nasdaq_institution(stock)
    return response
def parse_response(response):

    institution_date = map(lambda data: {data["label"]: data["value"]},response["data"]["ownershipSummary"].values() or [] )
    active_position_share_date = map(lambda data: {data["positions"]: data["shares"]},response["data"]["activePositions"]["rows"] or [] )
    active_position_holder_date = map(lambda data: {data["positions"]: data["holders"]},response["data"]["activePositions"]["rows"] or [] )
    new_position_share_date = map(lambda data: {data["positions"]: data["shares"]},response["data"]["newSoldOutPositions"]["rows"] or [] )
    new_position_holder_date = map(lambda data: {data["positions"]: data["holders"]},response["data"]["newSoldOutPositions"]["rows"] or [] )
    print(list(institution_date))
    print(list(active_position_share_date))
    print(list(active_position_holder_date))
    print(list(new_position_share_date))
    print(list(new_position_holder_date))


def insert_db(response):
    engine = mysql_connect.connect('sqlalchemy','stock', 'aws')
    # create session and add objects
    with Session(engine) as session:
        result = session.execute(select(StockInstitution))
        print(result)
        session.commit()

if __name__ == '__main__':
    try:
        main({"stock": "AAPL"})
    except KeyboardInterrupt:
        exit()