import json

data = {}

with open("data.json") as json_file:
    try:
        data = json.load(json_file)
    except ValueError:
        pass

if not data:
    print("There is no data.")

print(data)
