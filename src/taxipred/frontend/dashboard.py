import streamlit as st
from taxipred.utils.helpers import read_api_endpoint
from taxipred.utils.helpers import post_api_endpoint
from taxipred.utils.constants import ASSET_PATH
import pandas as pd
from taxipred.frontend.kpi_charts import kpi
from taxipred.frontend.background_code import add_background

st.set_page_config(page_title="Taxi Prediction Dashboard")#, page_icon=ASSET_PATH / "funny_taxi.png")
add_background()

data = read_api_endpoint("taxi")

df = pd.DataFrame(data.json())

def main():
    st.markdown("# Taxi Prediction Dashboard")
    labels, values = kpi()
    cols = st.columns(3)
    for col, lab, val in zip(cols, labels, values): 
        with col: 
            st.metric(label=lab, value=val)
        
    st.dataframe(df.head(2))
    st.divider()
    
    st.markdown("## Price prediction")

    # base_fare, per_km_rate, per_minute_rate = predict_rates()
    
    
    
    passenger_count = st.pills("Choose number of passengers", [1,2,3,4], default=1)#df['Passenger_Count'].sort_values().unique(), default=1)    
    time_day = st.pills("Choose time of day", df['Time_of_Day'].unique(), default="Morning")    
    day_week = st.pills("Choose day of week", df['Day_of_Week'].unique(), default="Weekday")
    traffic = st.pills("Choose traffic condition", df['Traffic_Conditions'].unique(), default="Low")
    weather = st.pills("Choose weather", df['Weather'].unique(), default="Clear")
    distance = st.select_slider("Choose trip distance in km", options=round(df["Trip_Distance_km"]).sort_values().unique())
    duration = st.select_slider("Choose trip duration in min", options=round(df["Trip_Duration_Minutes"]).sort_values().unique())

    # base_fare = df["Base_Fare"].median()
    # per_km_rate = df["Per_Km_Rate"].median()
    # per_minute_rate = df["Per_Minute_Rate"].median()
    
    objects_for_fares = {
            "Time_of_Day": time_day,
            "Day_of_Week": day_week,
            "Traffic_Conditions": traffic,
            "Weather": weather,
    }
    rate_predict = post_api_endpoint(objects_for_fares, "taxi/rate_predict").json()
    # st.write("Base Fare: ", rate_predict.get("Base_Fare"))
    # st.write("Min rate: ", rate_predict.get("Per_Minute_Rate"))
    # st.write("KM rate: ", rate_predict.get("Per_Km_Rate"))
    
    
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

    data_predict = post_api_endpoint(payload,"taxi/predict").json()
    predicted_price = round(data_predict.get("predicted_price") *9.41)
    # st.write("----------------------")
    st.divider()
    st.markdown(f"### Estimated price for your trip: {predicted_price} SEK")
    

    
if __name__ == "__main__":
    main()
