# Example using LightGBM
import lightgbm as lgb
import pandas as pd
from sklearn.model_selection import train_test_split

def train_regression_model(data_path: str):
    # Load processed data
    df = pd.read_csv(data_path)
    
    # Split features/target (target = price)
    X = df.drop(columns=['price', 'cadaster_nr']) # Features matrix
    y = df['price'] # Target vector
    
    # Train/validation split
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2)
    
    # LightGBM model
    params = {
        'objective': 'regression',
        'metric': 'rmse',
        'num_leaves': 31,
        'learning_rate': 0.05,
        'feature_fraction': 0.9
    }
    
    train_data = lgb.Dataset(X_train, label=y_train)
    val_data = lgb.Dataset(X_val, label=y_val)
    
    model = lgb.train(
        params,
        train_data,
        valid_sets=[val_data],
        num_boost_round=1000,
        early_stopping_rounds=50
    )
    
    return model