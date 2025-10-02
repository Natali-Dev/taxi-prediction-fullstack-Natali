import joblib
import pandas as pd
from xgboost import XGBRegressor
from sklearn.multioutput import MultiOutputRegressor


df = pd.read_csv("../src/taxipred/data/cleaned_data.csv", index_col=0)

df_encoded = pd.get_dummies(df, drop_first=True)
X= df_encoded[['Time_of_Day_Evening', 'Time_of_Day_Morning','Time_of_Day_Night', 'Day_of_Week_Weekend', 'Traffic_Conditions_Low','Traffic_Conditions_Medium', 'Weather_Rain', 'Weather_Snow']]
y = df_encoded[['Base_Fare', 'Per_Km_Rate','Per_Minute_Rate']]


model = MultiOutputRegressor(XGBRegressor(
    n_estimators=1000, #antal träd som byggs D100
    learning_rate=0.02, # Hur mkt varje nytt träd påverkar slutmodellen, lägre värden = stabilare men kräver fler träd. D0.3
    max_depth=4, #större värden = risk för overfitting, mindre värden = risk för underfitting D6
    min_child_weight=2, #minsta antal observationer för att skapa en ny nod, högre värden = mer konservativ D1
    subsample=0.7, # antal rader som används per träd, < 1 ger slump och mindre overfitting. D1
    colsample_bytree=0.9, #Andel features som används per träd D1
    gamma=0, #minsta förbättring för att göra en split, högre värde = färre splits D0
    reg_alpha=4, #L1 regularisering, gör modellen glesare D0
    reg_lambda=1, #L2 regularisering, straffar stora koefficienter, stabiliserar D1
    random_state=42, 
))

model.fit(X,y)
joblib.dump(model, "../src/taxipred/models/taxi_rates_XBGRegressor.joblib")