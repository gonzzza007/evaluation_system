import numpy as np
from sklearn.metrics import mean_squared_error

def find_optimal_weights(test_data: pd.DataFrame):
    """Grid search for best hybrid weights"""
    best_score = float('inf')
    best_weights = (0, 0)
    
    for rule_weight in np.linspace(0, 1, 11):
        hybrid_preds = []
        for _, row in test_data.iterrows():
            pred = (row['rule_based'] * rule_weight + 
                   row['regression'] * (1-rule_weight))
            hybrid_preds.append(pred)
        
        score = mean_squared_error(test_data['true_price'], hybrid_preds)
        if score < best_score:
            best_score = score
            best_weights = (rule_weight, 1-rule_weight)
    
    return best_weights