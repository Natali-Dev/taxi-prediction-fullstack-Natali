import joblib
from xgboost import XGBRegressor
import pandas as pd

df_original = pd.read_csv("../src/taxipred/data/cleaned_data.csv", index_col=0) #.drop(columns=['Weather','Time_of_Day', 'Day_of_Week', "Traffic_Conditions"])
df_encoded = pd.get_dummies(df_original, drop_first=True)
X, y = df_encoded.drop(columns="Trip_Price"), df_encoded["Trip_Price"]

model = XGBRegressor(
    n_estimators=1000, #antal träd som byggs D100
    learning_rate=0.02, # Hur mkt varje nytt träd påverkar slutmodellen, lägre värden = stabilare men kräver fler träd. D0.3
    max_depth=3, #större värden = risk för overfitting, mindre värden = risk för underfitting D6
    min_child_weight=2, #minsta antal observationer för att skapa en ny nod, högre värden = mer konservativ D1
    subsample=0.7, # antal rader som används per träd, < 1 ger slump och mindre overfitting. D1
    colsample_bytree=0.9, #Andel features som används per träd D1
    gamma=0, #minsta förbättring för att göra en split, högre värde = färre splits D0
    reg_alpha=4, #L1 regularisering, gör modellen glesare D0
    reg_lambda=1, #L2 regularisering, straffar stora koefficienter, stabiliserar D1
    random_state=42, 
    
) 
model.fit(X,y)

joblib.dump(model, "../src/taxipred/models/taxi_XBGRegressor.joblib", compress=("xz", 3), protocol=5)