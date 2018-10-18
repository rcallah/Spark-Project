
import json
import numpy as np
import pandas as pd

resp = 'C:/Users/calla/Documents/Spark-X-Lab/prosc/cases_output_json/cases_output_ner.json'
json_data = open(resp).read()

data = json.loads(json_data)
df = pd.DataFrame.from_dict(data['@data'])
