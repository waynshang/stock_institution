from datetime import datetime as dt
def get_label_data(api_response, label, commencement_date, end_date):
  commencement_date = dt.strptime(commencement_date, "%Y-%m-%d")
  end_date = dt.strptime(end_date, "%Y-%m-%d")
  label_data = api_response["data"][label]
  result = {}
  if not label_data: return result
  label_data = label_data["s"][0]
  if not label_data: return result
  for date_value in label_data:
    value =date_value[1]
    date = dt.strptime(date_value[0], "%Y-%m-%d")
    
    if date >= commencement_date and date <= end_date:
      result[date_value[0]] = float(value)
  return result
