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


### Ideas: 
- check if bad weather == more bookings/higher fare (rain = more trips)

