import pandas as pd
import joblib
from sklearn.metrics import mean_absolute_error, mean_squared_error

def evaluate_model(model_path: str, test_data_path: str):
    """Evaluate model performance"""
    
    # Load model and test data
    model = joblib.load(model_path)
    test_data = pd.read_csv(test_data_path)
    
    # Prepare data
    X_test = test_data.drop(columns=['target_price', 'cadaster_nr'])
    y_test = test_data['target_price']
    
    # Predict and evaluate
    predictions = model.predict(X_test)
    
    metrics = {
        'MAE': mean_absolute_error(y_test, predictions),
        'RMSE': mean_squared_error(y_test, predictions, squared=False),
        'R2': model.score(X_test, y_test)
    }
    
    return metrics