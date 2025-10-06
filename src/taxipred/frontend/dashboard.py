import streamlit as st
from taxipred.utils.helpers import read_api_endpoint
from taxipred.utils.helpers import post_api_endpoint
from taxipred.utils.constants import ASSET_PATH
import pandas as pd
from taxipred.frontend.kpi_charts import kpi
from taxipred.frontend.background_code import add_background
from taxipred.frontend.customer_view import customer_layout, get_address
from taxipred.frontend.company_view import company_layout
import datetime


st.set_page_config(page_title="Taxi Prediction")#, page_icon=ASSET_PATH / "funny_taxi.png")

add_background()

def main():
    data = read_api_endpoint("taxi")

    df = pd.DataFrame(data.json())

    view_choice = st.sidebar.radio("Välj vy", ["Resekollen AB", "Kund"])
    is_valid = True #default True
    st.markdown("# Taxi Prediction")
    
    if view_choice == "Resekollen AB":
        payload = company_layout(df)
        button = st.button("Predict")

        if button: 
            data_predict = post_api_endpoint(payload,"taxi/predict").json()
            predicted_price = round(data_predict.get("predicted_price") *9.41)
            st.divider()
            st.info(f"### Estimated price for your trip: {predicted_price} SEK", width=500)

    elif view_choice == "Kund": 
        # later = st.toggle("Travel later")
        pickup, dropoff, passenger_count = get_address()
        # continue_button = st.button("Continue")
        if pickup and dropoff:
            payload, distance, duration = customer_layout(pickup, dropoff, passenger_count)

            if distance < 1 or duration < 5: 
                st.info(f"Your trip is to short for prediction, pick a longer journey")
                is_valid = False
            elif distance > 50 or duration > 120: 
                st.info(f"Your trip is to long for prediction, pick a shorter journey")
                is_valid = False
            else: 
                is_valid = True #default True
                
            st.info(f"Your trip covers **{distance} km** and lasts **{duration} min**")

            if is_valid:
                button = st.button("Predict")

                if button: 
                    data_predict = post_api_endpoint(payload,"taxi/predict").json()
                    predicted_price = round(data_predict.get("predicted_price") *9.41)
                    st.divider()
                    st.info(f"### Estimated price for your trip: {predicted_price} SEK", width=500)


    
if __name__ == "__main__":
    main()
