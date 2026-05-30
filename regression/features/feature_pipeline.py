from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer

def create_feature_pipeline(X):
    """Create feature engineering pipeline"""
    
    # Define numeric and categorical features
    numeric_features = ['area', 'sale_date', 'epsg_x', 'epsg_y']
    categorical_features = [
        'maakond',
        'soilbodylabel',
        # 'soil_profile',  # too many unique values for current dataset size (~217 unique / 325 rows)
        # 'soil_mod',      # too many unique values for current dataset size (~105 unique / 325 rows)
    ]
    
    # Numeric feature pipeline
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    
    # Categorical feature pipeline
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    # Combine pipelines
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ]).set_output(transform="pandas")

    return preprocessor