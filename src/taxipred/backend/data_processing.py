from taxipred.utils.constants import TAXI_CSV_PATH
import pandas as pd
import json
from pprint import pp, pprint

class TaxiData:
    def __init__(self):
        self.df = pd.read_csv(TAXI_CSV_PATH)

    def to_json(self):
        return json.loads(self.df.to_json(orient = "records"))

# df = pd.read_csv(TAXI_CSV_PATH)
# # pp(df.head().to_json(orient="records"), indent=3)
# # df.to_json()
