from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error,mean_squared_error,root_mean_squared_error
import pandas as pd
def data_handler(X,y): 
    """
    Handels train|test|val|split
    -> X_train, X_test, X_val, y_train, y_test, y_val, X_train_full, y_train_full, scaled_X_train, scaled_X_test, scaled_X_val
    """

    X_train_full, X_test, y_train_full, y_test = train_test_split(X, y, test_size=0.1, random_state=42) #X_train_full använder du när du utvärderat alla modeller
    X_train, X_val, y_train, y_val = train_test_split(X_train_full, y_train_full, test_size=0.11, random_state=42)
    
    scaler = StandardScaler()

    scaler.fit(X_train)
    scaled_X_train = scaler.transform(X_train)
    scaled_X_test = scaler.transform(X_test)
    scaled_X_val = scaler.transform(X_val)

    return X_train, X_test, X_val, y_train, y_test, y_val, X_train_full, y_train_full, scaled_X_train, scaled_X_test, scaled_X_val #, y_train, y_test, y_val

def regressor_model(model, x_data_for_training, y_true_for_training, data_to_predict, y_true) -> pd.DataFrame:
    """trains data, and returns a df with linear metrics of predictions
    """
    model.fit(x_data_for_training, y_true_for_training)
    y_pred = model.predict(data_to_predict)

    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = root_mean_squared_error(y_true, y_pred)

    df_metric = pd.DataFrame([{"mae":mae,"mse":mse,"rmse": rmse}])
    # mae, mse, rmse
    return df_metric

from sklearn.multioutput import MultiOutputRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from xgboost import XGBRegressor
from sklearn.linear_model import RidgeCV
from sklearn.linear_model import ElasticNetCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, root_mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler

def linear_models(x_data_for_training, y_true_for_training, x_data_predict, y_true): 
    """
    -> DF with metrics
    """
    
    best_k = find_k(x_data_for_training,y_true_for_training,x_data_predict,y_true)
    print("K for KNeighboursRegressor: ", best_k)
    
    models = {
    "LinearRegression": LinearRegression(),
    "RidgeCV": RidgeCV(),
    "ElasticNetCV": ElasticNetCV(),
    "KNeighborsRegressor": KNeighborsRegressor(n_neighbors=best_k),
    "RandomForestRegressor": RandomForestRegressor(),
    "XGBRegressor": XGBRegressor()
    }

    result = []
    for key, model in models.items(): 
        model.fit(x_data_for_training, y_true_for_training)
        y_pred = model.predict(x_data_predict)
        
        mae = mean_absolute_error(y_true, y_pred)
        mse = mean_squared_error(y_true, y_pred)
        rmse = root_mean_squared_error(y_true, y_pred)
        r2 = r2_score(y_true, y_pred)
        result.append([key, mae, mse, rmse, r2])
        
        df_metric = pd.DataFrame(result, columns=["model", "mae", "mse", "rmse", "r2"])
    return df_metric
    
    
def find_k(scaled_X_train, y_train, scaled_X_val, y_val):
    error_list = []
    for k in range(1,100):
        model = KNeighborsRegressor(n_neighbors=k)
        model.fit(scaled_X_train, y_train)
        y_pred = model.predict(scaled_X_val) #OBS predicta på valideringsdatan! 
        error = root_mean_squared_error(y_val, y_pred) #/ error = root_mean_squared_error(y_val, y_pred)
        error_list.append(error)
    best_index = min(error_list)
    best_k = error_list.index(best_index) +1
    return best_k