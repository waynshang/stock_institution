import pandas as pd
import yfinance as yf


stockNo = "FB"
startDate = "2021-01-01"
stock = yf.Ticker(stockNo)
stock_df = pd.DataFrame(stock.history(period='ytd',interval='1d'))
stock_df = stock_df.reset_index()
# print("參考交易日天數: {} 天".format(len(stock_df)))
# print(stock_df.iloc[[0]])
# print(stock_df["Close"][0:10].mean())


#case 1 if increase percentage over x1b
# next day price will decrease
# next 5 day price will decrease
# next 10 day price will decrease
# next 20 day price will decrease
def main(stock_df):
  print("====start======")
  day_1 = 0
  day_5 = 0
  day_10 = 0
  day_20 = 0
  over_percentage_time = 0
  total_increase_percentage =0
  length = len(stock_df)
  for i in range(length):
    increase_percentage = cal_increase_percentage(i, stock_df)
    total_increase_percentage += increase_percentage
    if increase_percentage <  3: continue
    print(stock_df["Close"][i])
    print("increase_percentage: {}".format(increase_percentage))
    over_percentage_time += 1
    if length>i+1 and stock_df["Close"][i+1] < stock_df["Close"][i]: day_1+=1
    if length>i+5 and stock_df["Close"][i+5] < stock_df["Close"][i]:day_5+=1
    if length>i+10 and (stock_df["Close"][i+10] < stock_df["Close"][i]):day_10+=1
  print("next day price will decrease percentage: {}%".format(day_1/over_percentage_time*100))
  print("next 5 day price will decrease percentage: {}%".format(day_5/over_percentage_time*100))
  print("next 10 day price will decrease percentage: {}%".format(day_10/over_percentage_time*100))
  print("average_increase_percentage: {}".format(total_increase_percentage/length))  



def cal_increase_percentage(index, stock_data, type_price = "Close"):
  pre_index = index - 1
  if index == 0: return 0 
  return ((stock_data[type_price][index] - stock_data[type_price][pre_index])/stock_data[type_price][pre_index])* 100

def cal_moving_average(stock_data, days, index, type_price = "Close"):
  start_date = index-days
  if start_date <0: start_date = 0
  return stock_data["Close"][index-days:index].mean()

main(stock_df)