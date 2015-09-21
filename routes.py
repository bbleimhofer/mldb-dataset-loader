import json, csv, urllib, StringIO

rp = mldb.plugin.rest_params

if rp.verb == "POST" and rp.remaining == "/loadcsv":
    payload = json.loads(rp.payload)
    reader = csv.DictReader(open(urllib.urlretrieve(payload["url"])[0]))
    dataset = mldb.create_dataset(dict(id=str(payload["name"]), type="beh.mutable"))
    for i, row in enumerate(reader):
        values = []
        row_name = i
        for col in row:
            if col == "":
                row_name = row[col]
            else:
                values.append([col, row[col], 0])
        dataset.record_row(row_name, values)
    dataset.commit()
    mldb.plugin.set_return("yay")
else:
    raise Exception("404")

mldb.plugin.set_request_handler(request_handler)
