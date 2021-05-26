import requests
def get_nasdaq_institution(stock):
  try:
    my_headers = {'user-agent': 'PostmanRuntime/7.26.10', 'Connection': 'keep-alive'}
    url = "https://api.nasdaq.com/api/company/" + stock + "/institutional-holdings?limit=0&sortColumn=marketValue&sortOrder=DESC"
    # response = http.request('GET', url, header={"Connection": "keep-alive"})
    response =requests.get(url, headers = my_headers)
    return response.json()
  except Exception as error:
    print("{}".format(error))
    return None
