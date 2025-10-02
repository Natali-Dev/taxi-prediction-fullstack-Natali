import streamlit as st
from taxipred.utils.helpers import read_api_endpoint
from taxipred.utils.helpers import post_api_endpoint
from taxipred.utils.constants import ASSET_PATH
import pandas as pd
from taxipred.frontend.kpi_charts import kpi
from taxipred.frontend.background_code import add_background
from taxipred.frontend.customer_view import get_time_of_day,get_day_of_week,get_weather, get_traffic
import datetime
st.set_page_config(page_title="Taxi Prediction Dashboard")#, page_icon=ASSET_PATH / "funny_taxi.png")
add_background()
city = "Kiruna"
weather, temp = get_weather(city)

st.write(f"Temperatur just nu i {city}: {temp}")
city = "Göteborg" #default göteborg just nu
weather, temp = get_weather(city)
st.write(f"Temperatur just nu i {city}: {temp}")
data = read_api_endpoint("taxi")

df = pd.DataFrame(data.json())

view_choice = st.sidebar.radio("Välj vy", ["Resekollen AB", "Kund"])

def main():
    st.markdown("# Taxi Prediction Dashboard")
    if view_choice == "Resekollen AB":
        labels, values = kpi()
        cols = st.columns(3)
        for col, lab, val in zip(cols, labels, values): 
            with col: 
                st.metric(label=lab, value=val)
            
        st.dataframe(df.head(2))
        st.divider()
        
        st.markdown("## Price prediction")

        # base_fare, per_km_rate, per_minute_rate = predict_rates()
    
        passenger_count = st.pills("Choose number of passengers", [1,2,3,4], default=1) #Båda   
        time_day = st.pills("Choose time of day", df['Time_of_Day'].unique(), default="Morning") #DT now eller DT baserat på dag? Eller båda    
        day_week = st.pills("Choose day of week", df['Day_of_Week'].unique(), default="Weekday") #Basera på DT
        traffic = st.pills("Choose traffic condition", df['Traffic_Conditions'].unique(), default="Low") #Baseras på google-api
        weather = st.pills("Choose weather", df['Weather'].unique(), default="Clear") 
        distance = st.select_slider("Choose trip distance in km", options=round(df["Trip_Distance_km"]).sort_values().unique()) #bara för företag
        duration = st.select_slider("Choose trip duration in min", options=round(df["Trip_Duration_Minutes"]).sort_values().unique()) #bara för företag
    elif view_choice == "Kund": 
        later = st.toggle("Travel later")
        # if later: 
            # pass #någon slags klocka/
        # else: 
        time_day = get_time_of_day()
        day_week = get_day_of_week()
        weather, temp = get_weather(city)
        traffic = get_traffic()
        st.write("Time of Day: ", time_day)# time_day = st.pills("Choose time of day", df['Time_of_Day'].unique(), default="Morning") #DT now eller DT baserat på dag? Eller båda    
        st.write("Day of Week: ", day_week) #day_week = st.pills("Choose day of week", df['Day_of_Week'].unique(), default="Weekday") #Basera på DT
        st.write("Weather: ", weather, ". feels like: ", temp)#weather = st.pills("Choose weather", df['Weather'].unique(), default="Clear") #Baseras på weather API, stad på google-api
        st.write("Traffic: ", traffic)#traffic = st.pills("Choose traffic condition", df['Traffic_Conditions'].unique(), default="Low") #Baseras på google-api, eller bara rush mellan 07-8.30 och 16-18
        passenger_count = st.pills("Choose number of passengers", [1,2,3,4], default=1) #Ska denna vara här? En resa ska ju inte kosta mer bara för att man är fler passagerare i samma bil  
        st.selectbox("Åka från", " ")
        st.selectbox("Åka till", " ")
        distance, duration = 10, 15
        objects_for_fares = {
        "Time_of_Day": time_day,
        "Day_of_Week": day_week,
        "Traffic_Conditions": traffic,
        "Weather": weather,
}

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
    button = st.button("Predict")
    # st.write(payload)
# if button: 
    data_predict = post_api_endpoint(payload,"taxi/predict").json()
    predicted_price = round(data_predict.get("predicted_price") *9.41)
    st.divider()
    st.info(f"### Estimated price for your trip: {predicted_price} SEK", width=500)
    

    
if __name__ == "__main__":
    main()
    # st.write("Base Fare: ", rate_predict.get("Base_Fare"))
    # st.write("Min rate: ", rate_predict.get("Per_Minute_Rate"))
    # st.write("KM rate: ", rate_predict.get("Per_Km_Rate"))
    # base_fare = df["Base_Fare"].median()
    # per_km_rate = df["Per_Km_Rate"].median()
    # per_minute_rate = df["Per_Minute_Rate"].median()