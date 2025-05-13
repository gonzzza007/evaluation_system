import pandas as pd
from sklearn.metrics import mean_absolute_error, r2_score

def compare_models(test_data: pd.DataFrame):
    """Compare rule-based vs regression predictions"""
    results = []
    
    for _, row in test_data.iterrows():
        # Get ground truth
        true_price = row['actual_price']
        
        # Rule-based prediction
        rule_based_price = rule_based_predict(row.to_dict())
        
        # Regression prediction
        regression_price = regression_predict(row.to_dict())
        
        results.append({
            'property_id': row['cadaster_nr'],
            'true_price': true_price,
            'rule_based': rule_based_price,
            'regression': regression_price
        })
    
    df = pd.DataFrame(results)
    
    # Calculate metrics
    print(f"Rule-Based MAE: {mean_absolute_error(df['true_price'], df['rule_based'])}")
    print(f"Regression MAE: {mean_absolute_error(df['true_price'], df['regression'])}")
    
    print(f"\nRule-Based R²: {r2_score(df['true_price'], df['rule_based'])}")
    print(f"Regression R²: {r2_score(df['true_price'], df['regression'])}")
    
    return df