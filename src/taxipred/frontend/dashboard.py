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

    # Ha alla kolumner i selectboxes ? Nej
    # [X] Ha objekt-kolumner som knappar, och så får man lägga in trip_distance_km samt trip_duration_minutes - till att börja med
    # Sedan gör så du kan skriva plats A-B och klicka på knappar för object-kolumnerna. (st.pills)
    # Sedan kan du bara välja plats A-B, välja resa nu/resa senare (st.toggle) och bara isf klicka på object-knappar
    base_fare = 3
    per_km_rate = 1
    per_minute_rate = 1
    
    passenger_count = st.pills("Choose number of passangers", [1,2,3,4], default=1)#df['Passenger_Count'].sort_values().unique(), default=1)    
    time_day = st.pills("Choose time of day", df['Time_of_Day'].unique(), default="Morning")    
    day_week = st.pills("Choose day of week", df['Day_of_Week'].unique(), default="Weekday")
    traffic = st.pills("Choose traffic condition", df['Traffic_Conditions'].unique(), default="Low")
    weather = st.pills("Choose weather", df['Weather'].unique(), default="Clear")
    distance = st.select_slider("Choose trip distance in km", options=round(df["Trip_Distance_km"]).sort_values().unique())
    duration = st.select_slider("Choose trip duration in min", options=round(df["Trip_Duration_Minutes"]).sort_values().unique())

    # Predicta! 
    #[X] Ha fasta värden på alla fares till att börja med
    # Sedan basera fares på vilka objekt du valt
    
    #[X] Få in endpoint för att anropa, men datan måste ju skickas in dit också? 
    payload = {
    "Trip_Distance_km": distance,
    "Time_of_Day": time_day,
    "Day_of_Week": day_week,
    "Passenger_Count": passenger_count,
    "Traffic_Conditions": traffic,
    "Weather": weather,
    "Base_Fare": base_fare,
    "Per_Km_Rate": per_km_rate,
    "Per_Minute_Rate": per_minute_rate,
    "Trip_Duration_Minutes": duration,
    }

    data_predict = post_api_endpoint(payload,"taxi/predict").json()
    predicted_price = round(data_predict.get("predicted_price") *9.41)
    # st.write("----------------------")
    st.divider()
    st.markdown(f"### Estimated price for your requirements: {predicted_price} SEK")
    

    
if __name__ == "__main__":
    main()
