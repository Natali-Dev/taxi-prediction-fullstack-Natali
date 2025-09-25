from fastapi import FastAPI
from taxipred.utils.constants import TAXI_MODEL_PATH,CLEANED_TAXI_CSV_PATH, dictionary_for_encoding
from taxipred.backend.data_processing import TaxiData, Taxi, TaxiPrediction
from pprint import pp
import pandas as pd
import joblib
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.df = pd.read_csv(CLEANED_TAXI_CSV_PATH) #startup
    app.state.model = joblib.load(TAXI_MODEL_PATH)
    yield #app running
    del app.state.df #on shutdown
    del app.state.model

app = FastAPI()

taxi_data = TaxiData() #Instans av klassen, en df, innehåller self.df
# print(taxi_data.df.head())

@app.get("/taxi")
async def read_taxi_data():
    return taxi_data.to_json() #df.to_json-metod från klassen, orient=records

@app.get("/taxi/summary")
def read_summary():
    return taxi_data.df.describe().T.to_dict()

# I NB får man ut en np-array. 
@app.post("/taxi/predict", response_model=TaxiPrediction) #Vilken typ av output den ska returna när man skickat in värden att predicta
def predict_taxi_price(payload: Taxi): #man kan säga att payload = userinput, alltså de värden användaren lägger in som de vill ha predictade
    dictionary_for_encoding.append(payload.model_dump()) #Måste konvertera payload som är ett pydantic-object till en dict, med model_dump! 
    
    data_to_predict = pd.DataFrame(dictionary_for_encoding)
    encoded_data_to_predict = pd.get_dummies(data_to_predict, drop_first=True)
    model = joblib.load(TAXI_MODEL_PATH)
    y_pred = model.predict(encoded_data_to_predict.tail(1)) #predicta på den sista dictionaryn!
    return {"predicted_price": y_pred[0]}
    # y_pred = model.predict(pd.DataFrame([encoded_data_to_predict.iloc[4]])) #predicta på den sista dictionaryn!
    # return data_to_predict

@app.post("/taxi/add_trip")
def add_trip():
    pass


# predict_taxi_price(taxi_data.df.to_json())
# pp(taxi_data.df.iloc[0])
# pp(taxi_data.df['Time_of_Day'].unique())
# pp(taxi_data.df['Day_of_Week'].unique())
# pp(taxi_data.df['Traffic_Conditions'].unique())
# pp(taxi_data.df['Weather'].unique())