# taxi-prediction-fullstack-Natali
Labb OOP 1

A project for predicting. The backend and frontend will communicate thru an API-layer to make the components decoupled. The application will serve a ML-model and make relevant predictions. 


### About the columns: 

- Distance (in kilometers): The length of the trip.
- Time of Day: The time of day the trip started (Morning, Afternoon, Evening, or Night).
- Day of Week: Indicates whether the trip took place on a Weekday or Weekend.
- Traffic Condition: Categorical indicator of traffic (low, medium, high).
- Passenger Count: Number of passengers for the trip. (1-4)
- Weather Condition: Categorical data for weather (clear, rain, snow).
- Trip Duration Minutes: Total trip time.
- Trip_Price (target): The cost of the trip (in USD).

Fares: 
- Base_Fare: The initial base fare of the taxi ride before any distance or time charges.
- Per_Km_Rate: The rate charged per kilometer of the trip.
- Per_Minute_Rate: The rate charged per minute of the trip duration.

# Explaining the structure

###  setup.py 
- For packaging the module: enables importing files freely from different places. If installed it will also insall librarys that are specified. Use pip to install.
## /explorations
- **final_cleaning.ipynb** - where the final cleaning took place (no testing, only logic). 
- The other Jupyter notebooks are only explorations and files for testing.

##  /backend
- **api.py** - contains FastAPI and different endpoints. An interface.
- **data_processing.py** - class TaxiData for reading the dataframe and method for converting dataframe to json-format. Pydantic classes for validating data.  
- **predict_fares.py** - model training and exporting for predicting base rate and fares. Uses the object columns as features. 
- **predict_trip_price.py** - model training and exporting for predicting trip price, uses all other columns as features. 

##  /frontend
- **background_code.py** - chatgpt generated CSS code for making a dark box over the page, so the background only is 100% visible in the margins. 
- **company_view.py** - logic for the company page. Here you can select different values for all the feature columns (except rate and fares) to get a prediction for the trip price. 
- **customer_view.py** - logic for the customer page. Uses OpenWeather API for getting current weather and getting the city by sending in longitude and latitude from Google API. Google API, the user select from/to addresses and total distance and duration between them are taken from the dictionary that the response contains, alos longitude and latitude.
- **dashboard.py** - methods from company and customer view are called here, and has code wich applies to both views.
- **kpi_charts.py** - has 3 kpis, an empty chart function for later development.

##  /utils
- **constants.py** - has filepaths and a dictionary which is used in api.py, for encoding. The model is trained on encoded data, so it requiers all columns to be the same when predicting. 
- **helpers.py** - functions for sending read and post requests to the backend, called in frontend.py. Theese functions connects the backend localhost url to the frontend. 