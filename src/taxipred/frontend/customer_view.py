import streamlit as st
from taxipred.utils.helpers import read_api_endpoint
from taxipred.utils.helpers import post_api_endpoint
from taxipred.utils.constants import ASSET_PATH
import pandas as pd
from taxipred.frontend.kpi_charts import kpi
from taxipred.frontend.background_code import add_background
from dotenv import load_dotenv
import os, requests, datetime, json
time_now = datetime.datetime.now()
def customer(): 
    pass

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

def get_weather(city):
    load_dotenv()
    API_KEY = os.getenv("weather_api")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url)
    output = json.loads(response.text)
    weather = output["weather"][0]["main"]
    if weather == "Clouds":
        weather = "Clear"
        return weather, output["main"]["feels_like"]
    else:
        return output["weather"][0]["main"], output["main"]["feels_like"]
    
def get_traffic(): 
    if time_now.hour > 8 < 18:
        traffic = "Medium"
        if time_now.hour == 7 or time_now.hour == 15 or time_now.hour == 16: 
            traffic = "High"
    else: 
        traffic = "Low"
    return traffic