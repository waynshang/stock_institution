def row2list(model, rows, exclude_columns):
    d = []
    for row in rows:
      d.append(model2dict(model, data, exclude_columns))
    return d

def model2dict(model, data, exclude_columns):
    print("model2dict")
    columns = list(set(model.__table__.columns.keys())-set(exclude_columns))
    print(columns)
    return {c: getattr(data, c) for c in columns}
