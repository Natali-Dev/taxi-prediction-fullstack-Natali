from taxipred.utils.constants import CLEANED_TAXI_CSV_PATH
import pandas as pd
import json
from pprint import pp, pprint
from pydantic import BaseModel, Field
from typing import Literal

class TaxiData:
    def __init__(self):
        self.df = pd.read_csv(CLEANED_TAXI_CSV_PATH, index_col=0)


    def to_json(self):
        return json.loads(self.df.to_json(orient = "records"))

class Taxi(BaseModel):
    
    # 'Trip_Distance_km', 'Passenger_Count', 'Base_Fare', 'Per_Km_Rate','Per_Minute_Rate', 'Trip_Duration_Minutes', 'Trip_Price','Time_of_Day_Evening', 'Time_of_Day_Morning', 'Time_of_Day_Night','Day_of_Week_Weekend', 'Traffic_Conditions_Low','Traffic_Conditions_Medium', 'Weather_Rain', 'Weather_Snow'
    # 'Trip_Distance_km', 'Passenger_Count', 'Base_Fare', 'Per_Km_Rate',
    #    'Per_Minute_Rate', 'Trip_Duration_Minutes', 'Trip_Price'
    
    Trip_Distance_km: float = Field(ge=1 ,le=1000)	
    Time_of_Day: Literal['Morning', 'Evening', 'Afternoon', 'Night']	
    Day_of_Week: Literal['Weekday', 'Weekend']	
    Passenger_Count: int = Field(ge= 1 ,le=4)	
    Traffic_Conditions: Literal['Low', 'High', 'Medium']	
    Weather: Literal['Clear', 'Rain', 'Snow']
    Base_Fare: float = Field(ge= 1,le=10)	
    Per_Km_Rate: float = Field(ge= 0,le=10)	
    Per_Minute_Rate: float = Field(ge= 0,le=10)	
    Trip_Duration_Minutes: float = Field(ge= 0,le=180)	

class TaxiPrediction(BaseModel):
    predicted_price: float #TODO kanske field här? 
    
# df = pd.read_csv(TAXI_CSV_PATH)
# # df.to_json()
