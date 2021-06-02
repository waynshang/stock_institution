from datetime import date, datetime

def row2list(model, rows, exclude_columns):
    d = []
    for row in rows:
      d.append(model2dict(model, data, exclude_columns))
    return d

def model2dict(model, data, exclude_columns):
    columns = list(set(model.__table__.columns.keys())-set(exclude_columns))
    return {c: getattr(data, c) for c in columns}

def insert_or_update(session, data, symbol, model, log_model, query_results, exclude_columns, log_exclude_columns):
    if data:
      data["symbol"] = symbol
      data["date"] = date.today()
      log_data = {"symbol": symbol, "updated_at": datetime.now()}
      if query_results.first():
          query_result = query_results.first()
          log_data["date"] = vars(query_result)["date"]
          print("======last update date: {} ======".format(vars(query_result)["date"]))
          if vars(query_result)["date"] != date.today():
            compared_columns = list(set(data.keys())-set(exclude_columns))
            for column in compared_columns:
              log_data[column] = float(data[column]) - float(vars(query_result)[column])
            data["updated_at"] = datetime.now()
            log_data = model2dict(model, query_result, log_exclude_columns)
            # print(log_data)
            session.add(log_model(**log_data))
            query_results.update(data)
      else:
          data["updated_at"] = datetime.now()
          session.add(model(**data))
      return session
