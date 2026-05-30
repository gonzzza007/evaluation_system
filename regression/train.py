import pandas as pd
import joblib
from lightgbm import LGBMRegressor
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score
from pathlib import Path
from regression.features.feature_pipeline import create_feature_pipeline

def train_and_save_model(
    data_path: Path,
    model_save_path: Path,
    config_path: Path
):
    df = pd.read_parquet(data_path)

    X = df.drop(columns=['price'])
    y = df['price']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"Train: {len(X_train)} samples, Test: {len(X_test)} samples")

    feature_pipeline = create_feature_pipeline(X_train)

    model = LGBMRegressor(
        num_leaves=31,
        learning_rate=0.05,
        n_estimators=1000,
        objective='mape',
    )

    full_pipeline = Pipeline([
        ('features', feature_pipeline),
        ('model', model)
    ])

    full_pipeline.fit(X_train, y_train)

    # Save test set with original prices for evaluate.py
    test_df = X_test.copy()
    test_df['price'] = y_test
    test_save_path = data_path.parent / 'test_data.parquet'
    test_df.to_parquet(test_save_path)

    predictions = full_pipeline.predict(X_test)
    print(f"Test MAE:  {mean_absolute_error(y_test, predictions):.0f}")
    print(f"Test RMSE: {root_mean_squared_error(y_test, predictions):.0f}")
    print(f"Test R²:   {r2_score(y_test, predictions):.3f}")

    joblib.dump(full_pipeline, model_save_path)
    print(f"Model saved to {model_save_path}")

if __name__ == "__main__":
    # Configure paths
    DATA_PATH = Path("data/training_data.parquet")
    MODEL_SAVE_PATH = Path("regression/models/saved_models/latest_model.pkl")
    CONFIG_PATH = Path("configs/regression_params.yaml")
    
    train_and_save_model(DATA_PATH, MODEL_SAVE_PATH, CONFIG_PATH)