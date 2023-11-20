import pandas as pd
import json

ids = [200,300,500,600,800,801,802,803,804]

images = [
    ['raining_cloud', 'cloud_lightning'],
    ['raining_cloud'],
    ['raining_cloud'],
    ['snowflake'],
    ['sun'],
    ['sun', 'cloud'],
    ['sun', 'cloud'],
    ['cloud', 'sun'],
    ['cloud']
          ]

weather = {}
for c, code in enumerate(ids):
    weather[code] = images[c]

# Convert and write JSON object to file
with open(r"C:\Users\josep\Desktop\smartAC\weather.json", "w") as outfile:
    json.dump(weather, outfile)