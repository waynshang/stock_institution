from datetime import date, datetime

def row2list(model, rows, exclude_columns):
    d = []
    for row in rows:
      d.append(model2dict(model, row, exclude_columns))
    return d

def model2dict(model, data, exclude_columns):
    columns = list(set(model.__table__.columns.keys())-set(exclude_columns))
    return {c: getattr(data, c) for c in columns}

def update_table_and_insert_log(session, data_from_api, symbol, model, log_model):
  if not data_from_api: return session
  log_exclude_columns = log_model.EXCLUDE_COLUMNS

  data_filter_by_symbol = model.get_data_by_column(session, symbol, 'symbol')

  data_from_api["symbol"] = symbol
  data_from_api["date"] = date.today()

  # log_data = {"symbol": symbol, "updated_at": datetime.now()}
  if data_filter_by_symbol:
    #need to add to log table
    old_data = model2dict(model, data_filter_by_symbol, log_exclude_columns)
    # DEBUG.info(old_data)
    # DEBUG.info("======last update date: {} ======".format(vars(data_filter_by_symbol)["date"]))
    if vars(data_filter_by_symbol)["date"] != date.today():
      session = log_model.prepare_and_data_from_api(session, data_from_api, old_data)
      # data_from_api["updated_at"] = datetime.now()      
      data_filter_by_symbol.updated_at = datetime.now() 
  else:
      data_from_api["updated_at"] = datetime.now()
      session.add(model(**data_from_api))
  return session


