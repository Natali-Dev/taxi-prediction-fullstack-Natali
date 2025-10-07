import streamlit as st
from taxipred.utils.helpers import post_api_endpoint
from dotenv import load_dotenv
import os, requests, datetime, json
time_now = datetime.datetime.now()

def get_time_of_day():
    # morning 4-12, afternoon 12-18, evening 18-23, night 23-04
    if time_now.hour > 4 < 12: 
        time_day = "Morning"
    if time_now.hour > 12 < 18: 
        time_day = "Afternoon"
    if time_now.hour > 18 < 23: 
        time_day = "Evening"
    if time_now.hour > 23 < 4: 
        time_day = "Night"
    return time_day

def get_day_of_week():
    day = time_now.weekday()
    if day < 6:
        day_week = "Weekday"
    else: 
        day_week = "Weekend"
    return day_week

def get_weather(latitude, longitude):
    load_dotenv()
    API_KEY = os.getenv("weather_api")
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={API_KEY}&units=metric"

    response = requests.get(url)
    output = json.loads(response.text)
    weather = output["weather"][0]["main"]
    if weather == "Clear" or weather == "Rain" or weather == "Snow":
        return output["weather"][0]["main"], output["main"]["feels_like"], output["name"]
    elif weather == "Drizzle" or weather == "Clouds": 
        weather = "Rain"
        return weather, output["main"]["feels_like"], output["name"]
    else:
        weather = "Clear"
        return weather, output["main"]["feels_like"], output["name"]
    
def get_traffic(data): 
    duration, duration_in_traffic = data["routes"][0]["legs"][0]["duration"], data["routes"][0]["legs"][0]["duration_in_traffic"]
    
    diff = round(duration["value"] / 60) - round(duration_in_traffic["value"] / 60)
    
    if diff < 2: 
        traffic = "Low"
    elif diff <= 5:
        traffic = "Medium"
    else: 
        traffic = "High"
    return traffic

def get_google(pickup, dropoff):
    load_dotenv()
    unix_now = int(datetime.datetime.now().timestamp())
    API_KEY = os.getenv("google_api")
    
    url = ("https://maps.googleapis.com/maps/api/directions/json?"
    f"origin={pickup}&destination={dropoff}&mode=driving&key={API_KEY}&departure_time={unix_now}")

    response = requests.get(url).json()

    return response
def get_address():
    pickup = st.selectbox("Going from", ["Östanvindsgatan, Göteborg", "Centralstationen, Göteborg"], index=None, placeholder="Select an address or enter a new one", accept_new_options=True)
    dropoff = st.selectbox("Going to", ["Liseberg, Göteborg", "Konstmuseeum, Göteborg"], index=None, placeholder="Select an address or enter a new one", accept_new_options=True)
    passenger_count = st.pills("Choose number of passengers", [1,2,3,4], default=1) #Ska denna vara här? En resa ska ju inte kosta mer bara för att man är fler passagerare i samma bil. Man skulle kunna ha 1 bara, eftersom det inte har så mycket med en resa just nu att göra. Uppenbarligen tenderar resorna bli längre vid fler passagerare.  
    
    return pickup, dropoff, passenger_count
    

def customer_layout(pickup, dropoff, passenger_count):
    response = get_google(pickup, dropoff)
    distance_value = response["routes"][0]["legs"][0]["distance"]
    duration_value = response["routes"][0]["legs"][0]["duration_in_traffic"] 
    distance = round(distance_value["value"] / 1000,2)
    duration = round(duration_value["value"] / 60)

    city = response["routes"][0]["legs"][0]["end_location"]
    
    latitude = city["lat"]
    longitude = city["lng"]
    weather, temp, city = get_weather(latitude, longitude)
    time_day = get_time_of_day()
    day_week = get_day_of_week()
    traffic = get_traffic(response)
    st.markdown("### Current conditions")

    col1,col2,col3 = st.columns(3)
    col1.markdown(f"**Traffic:** {traffic}") 
    col2.markdown(f"**Day of week:** {day_week}")
    col3.markdown(f"**Time of day:** {time_day}")
    col1.markdown(f"**City:** {city}")
    col2.markdown(f"**Weather:** {weather}")
    col3.markdown(f"**Temperature:** {temp} °C") 

    objects_for_fares = {
            "Time_of_Day": time_day,
            "Day_of_Week": day_week,
            "Traffic_Conditions": traffic,
            "Weather": weather,
    }
    rate_predict = post_api_endpoint(objects_for_fares, "taxi/rate_predict").json()

    payload = {
    "Trip_Distance_km": distance,
    "Time_of_Day": time_day,
    "Day_of_Week": day_week,
    "Passenger_Count": passenger_count,
    "Traffic_Conditions": traffic, #Get med google API
    "Weather": weather, #Get med weather API
    "Base_Fare": rate_predict.get("Base_Fare"), #predictade rates gör mindre variation i priset när man predictar dem, för att de balanseras nu mot objektkolumnerna, om det är tex rain = mer/längre resor = lägre priser.
    "Per_Km_Rate": rate_predict.get("Per_Km_Rate"),
    "Per_Minute_Rate": rate_predict.get("Per_Minute_Rate"),
    "Trip_Duration_Minutes": duration,
    }

    return payload, distance, duration

    # st.write("Time of Day: ", time_day)# time_day = st.pills("Choose time of day", df['Time_of_Day'].unique(), default="Morning") #DT now eller DT baserat på dag? Eller båda    
    # st.write("Day of Week: ", day_week) #day_week = st.pills("Choose day of week", df['Day_of_Week'].unique(), default="Weekday") #Basera på DT
    # st.write("Weather: ", weather, ". feels like: ", temp)#weather = st.pills("Choose weather", df['Weather'].unique(), default="Clear") #Baseras på weather API, stad på google-api
    # st.write("Traffic: ", traffic)#traffic = st.pills("Choose traffic condition", df['Traffic_Conditions'].unique(), default="Low") #Baseras på google-api, eller bara rush mellan 07-8.30 och 16-18