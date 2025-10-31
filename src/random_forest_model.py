import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

def rf_model(data):
    features = ["N", "P", "K", "OC", "ph"] # h in ph is small in the dataset
    X = data[features].values # matrix
    y = data["SFI"].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size = 0.2, random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=15,
        min_samples_split = 5,
        random_state=42,
        n_jobs = -1
    )
    model.fit(X_train, y_train)

    r2_train = model.score(X_train, y_train)
    y_predict = model.predict(X_test)
    r2_test = r2_score(y_test, y_predict)
    rmse = np.sqrt(mean_squared_error(y_test, y_predict)) 

    importances = model.feature_importances_
    features_importances_dict = { 
        feat : imp for feat, imp in sorted(zip(features, importances), key=lambda x: x[1], reversed=True)
    }
    
    return model, features
