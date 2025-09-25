from importlib.resources import files

# 'files' tar namnet för paketet (vi har satt name="taxipred" i setup.py)
# får tillbaka ett resource-träd med alla filer i paketet (Traversable)
# 'joinpath' skapar sedan en sökväg inne i paketet
# och vår Traversable(resultatet) ser ut såhär: <project-root>/src/taxipred/data/taxi_trip_pricing.csv

# files = taxipred innebär att vi väljer den mappen, och lägger till sökvägen data/...
TAXI_CSV_PATH = files("taxipred").joinpath("data/taxi_trip_pricing.csv")
CLEANED_TAXI_CSV_PATH = files("taxipred").joinpath("data/cleaned_data.csv")
# DATA_PATH = Path(__file__).parents[1] / "data"

TAXI_MODEL_PATH = files("taxipred").joinpath("models/taxi_XBGRegressor.joblib")
ASSET_PATH = files("taxipred").joinpath("assets/")
dictionary_for_encoding = [
{
"Trip_Distance_km": 1,
"Time_of_Day": "Morning",
"Day_of_Week": "Weekday",
"Passenger_Count": 1,
"Traffic_Conditions": "Low",
"Weather": "Clear",
"Base_Fare": 1,
"Per_Km_Rate": 10,
"Per_Minute_Rate": 10,
"Trip_Duration_Minutes": 180,
},
{
"Trip_Distance_km": 1,
"Time_of_Day": "Evening",
"Day_of_Week": "Weekend",
"Passenger_Count": 1,
"Traffic_Conditions": "High",
"Weather": "Rain",
"Base_Fare": 1,
"Per_Km_Rate": 10,
"Per_Minute_Rate": 10,
"Trip_Duration_Minutes": 180,
},
{
"Trip_Distance_km": 1,
"Time_of_Day": "Afternoon",
"Day_of_Week": "Weekday",
"Passenger_Count": 1,
"Traffic_Conditions": "Medium",
"Weather": "Snow",
"Base_Fare": 1,
"Per_Km_Rate": 10,
"Per_Minute_Rate": 10,
"Trip_Duration_Minutes": 180,
},

{

"Trip_Distance_km": 1,
"Time_of_Day": "Night",
"Day_of_Week": "Weekday",
"Passenger_Count": 1,
"Traffic_Conditions": "Low",
"Weather": "Clear",
"Base_Fare": 1,
"Per_Km_Rate": 10,
"Per_Minute_Rate": 10,
"Trip_Duration_Minutes": 180,
}
]