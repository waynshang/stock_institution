from yahoofinancials import YahooFinancials
from datetime import datetime
from openpyxl import Workbook

def main():
  wb = Workbook()
  # grab the active worksheet
  ws = wb.active
  

  tickers = ['AAPL' , 'QQQ', 'SPY']
  header = ['Date']
  price_data_by_date = {}
  volume_data_by_date = {}
  header += (tickers + tickers)
  for ticker in tickers:
    
   
    yahoo_financials = YahooFinancials(ticker)
    price_date = yahoo_financials.get_historical_price_data('2000-01-01', datetime.now().strftime('%Y-%m-%d'), 'weekly')
    price_data = price_date[ticker]['prices']
    for index, price in enumerate(price_data):
      
      if index == 0 or (price['close'] is None): 
        print(ticker)
        print(price)
        print(index == 0)
        print(price['close'] is None)
        continue

      date = price['formatted_date']
      prev_price = price_data[index-1]['close'] if index > 0 else price['close']
      prev_volume = price_data[index-1]['volume'] if index > 0 else price['volume']

      price_change = round(((price['close'] - prev_price) / prev_price) * 100,2 )
      volume_change = round(((price['volume'] - prev_volume) / prev_volume) * 100 ,2 )

      if date in price_data_by_date:
        price_data_by_date[date] = price_data_by_date[date] + [price_change]
        volume_data_by_date[date] = volume_data_by_date[date] + [volume_change]
      else:
        price_data_by_date[date] = [date, price_change]
        volume_data_by_date[date] = [volume_change]


  ws.append(header)
  for date, data in price_data_by_date.items():
    ws.append(data+volume_data_by_date[date])
  
  wb.save("change.xlsx")

if __name__ == "__main__":
  main()