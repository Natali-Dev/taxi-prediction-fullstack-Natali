from taxipred.utils.constants import CLEANED_TAXI_CSV_PATH
import pandas as pd
import json
from pydantic import BaseModel, Field
from typing import Literal

class TaxiData:
    def __init__(self):
        self.df = pd.read_csv(CLEANED_TAXI_CSV_PATH, index_col=0)


    def to_json(self):
        return json.loads(self.df.to_json(orient = "records"))

class Taxi(BaseModel):
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

class TaxiRate(BaseModel): #Detta är "X"
    Time_of_Day: Literal['Morning', 'Evening', 'Afternoon', 'Night'] 
    Weather: Literal['Clear', 'Rain', 'Snow']
    Day_of_Week: Literal['Weekday', 'Weekend'] 
    Traffic_Conditions: Literal['Low', 'High', 'Medium']

class TaxiRatePrediction(BaseModel): # Detta är "Y"
    Base_Fare: float = Field(ge=0, lt=10)
    Per_Km_Rate: float = Field(ge=0, lt=10)
    Per_Minute_Rate: float = Field(ge=0, lt=10)

class TaxiPrediction(BaseModel):
    predicted_price: float #TODO kanske field här? 
    


