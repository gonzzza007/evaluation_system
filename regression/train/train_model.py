import pandas as pd
import joblib
from lightgbm import LGBMRegressor
from sklearn.pipeline import Pipeline
from pathlib import Path
from .features.feature_pipeline import create_feature_pipeline

def train_and_save_model(
    data_path: Path,
    model_save_path: Path,
    config_path: Path
):
    """Main training workflow"""
    
    # 1. Load and preprocess data
    df = pd.read_csv(data_path)
    
    # 2. Split features/target
    X = df.drop(columns=['target_price', 'cadaster_nr'])
    y = df['target_price']
    
    # 3. Create feature engineering pipeline
    feature_pipeline = create_feature_pipeline(X)
    
    # 4. Define model with hyperparameters
    model = LGBMRegressor(
        num_leaves=31,
        learning_rate=0.05,
        n_estimators=1000
    )
    
    # 5. Create full pipeline
    full_pipeline = Pipeline([
        ('features', feature_pipeline),
        ('model', model)
    ])
    
    # 6. Train model
    full_pipeline.fit(X, y)
    
    # 7. Save trained model
    joblib.dump(full_pipeline, model_save_path)
    print(f"Model saved to {model_save_path}")

if __name__ == "__main__":
    # Configure paths
    DATA_PATH = Path("data/processed/training_data.csv")
    MODEL_SAVE_PATH = Path("regression/models/saved_models/latest_model.pkl")
    CONFIG_PATH = Path("configs/regression_params.yaml")
    
    train_and_save_model(DATA_PATH, MODEL_SAVE_PATH, CONFIG_PATH)