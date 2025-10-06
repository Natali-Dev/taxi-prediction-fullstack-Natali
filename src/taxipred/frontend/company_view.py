import streamlit as st
from taxipred.utils.helpers import post_api_endpoint
from taxipred.frontend.kpi_charts import kpi


def company_layout(df):
    labels, values = kpi(df)
    cols = st.columns(3)
    for col, lab, val in zip(cols, labels, values): 
        with col: 
            st.metric(label=lab, value=val)
            
    st.divider()
        
    st.markdown("## Price prediction")
    
    passenger_count = st.pills("Choose number of passengers", [1,2,3,4], default=1) #Båda   
    time_day = st.pills("Choose time of day", df['Time_of_Day'].unique(), default="Morning") #DT now eller DT baserat på dag? Eller båda    
    day_week = st.pills("Choose day of week", df['Day_of_Week'].unique(), default="Weekday") #Basera på DT
    traffic = st.pills("Choose traffic condition", df['Traffic_Conditions'].unique(), default="Low") #Baseras på google-api
    weather = st.pills("Choose weather", df['Weather'].unique(), default="Clear") 
    distance = st.select_slider("Choose trip distance in km", options=round(df["Trip_Distance_km"]).sort_values().unique()) #bara för företag
    duration = st.select_slider("Choose trip duration in min", options=round(df["Trip_Duration_Minutes"]).sort_values().unique()) #bara för företag
    
    objects_for_fares = {
            "Time_of_Day": time_day,
            "Day_of_Week": day_week,
            "Traffic_Conditions": traffic,
            "Weather": weather,
    }
    rate_predict = post_api_endpoint(objects_for_fares, "taxi/rate_predict").json()
    col1, col2, col3 = st.columns(3)
    col1.info(f"Base Fare: {round(rate_predict.get("Base_Fare")*9.41,2)} SEK")
    col2.info(f"Per Km Rate: {round(rate_predict.get("Per_Km_Rate")*9.41,2)} SEK")
    col3.info(f"Per Minute Rate: {round(rate_predict.get("Per_Minute_Rate")*9.41,2)} SEK")
    payload = {
    "Trip_Distance_km": distance,
    "Time_of_Day": time_day,
    "Day_of_Week": day_week,
    "Passenger_Count": passenger_count,
    "Traffic_Conditions": traffic, 
    "Weather": weather, 
    "Base_Fare": rate_predict.get("Base_Fare"), #predictade rates gör mindre variation i priset när man predictar dem, för att de balanseras nu mot objektkolumnerna, om det är tex rain = mer/längre resor = lägre priser.
    "Per_Km_Rate": rate_predict.get("Per_Km_Rate"),
    "Per_Minute_Rate": rate_predict.get("Per_Minute_Rate"),
    "Trip_Duration_Minutes": duration,
    }
    
    return payload