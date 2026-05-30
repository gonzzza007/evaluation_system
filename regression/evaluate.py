import pandas as pd
import joblib
from pathlib import Path
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score


def evaluate_model(model_path: str, test_data_path: str):
    model = joblib.load(model_path)
    path = Path(test_data_path)
    test_data = pd.read_parquet(path) if path.suffix == '.parquet' else pd.read_csv(path)

    X_test = test_data.drop(columns=['price'])
    y_test = test_data['price']

    predictions = model.predict(X_test)

    return {
        'MAE': mean_absolute_error(y_test, predictions),
        'RMSE': root_mean_squared_error(y_test, predictions),
        'R2': r2_score(y_test, predictions)
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Evaluate trained regression model')
    parser.add_argument('--model', default='regression/models/saved_models/latest_model.pkl')
    parser.add_argument('--test-data', default='data/test_data.parquet')
    args = parser.parse_args()

    metrics = evaluate_model(args.model, args.test_data)
    for name, value in metrics.items():
        print(f"{name}: {value:.4f}")
