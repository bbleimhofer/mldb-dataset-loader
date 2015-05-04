import json, csv, urllib, StringIO

mldb.plugin.serve_static_folder('/static', 'static')
mldb.plugin.serve_documentation_folder('doc')

def request_handler(mldb, remaining, verb, resource, rest_params, payload,
                    content_type, content_length, headers):
    if verb == "POST" and remaining == "/loadcsv":
        payload = json.loads(payload)
        reader = csv.DictReader(open(urllib.urlretrieve(payload["url"])[0]))
        dataset = mldb.create_dataset(dict(id=str(payload["name"]), type="beh_mutable"))
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
        return "yay"
    else:
        raise Exception("404")

mldb.plugin.set_request_handler(request_handler)
