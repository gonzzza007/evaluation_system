import matplotlib.pyplot as plt
import seaborn as sns

def plot_comparison(results_df: pd.DataFrame):
    plt.figure(figsize=(12, 6))
    
    # Error distribution
    plt.subplot(1, 2, 1)
    sns.kdeplot(results_df['true_price'] - results_df['rule_based'], label='Rule-Based')
    sns.kdeplot(results_df['true_price'] - results_df['regression'], label='Regression')
    plt.title("Error Distribution")
    
    # Actual vs Predicted
    plt.subplot(1, 2, 2)
    sns.scatterplot(x='true_price', y='rule_based', data=results_df, label='Rule-Based')
    sns.scatterplot(x='true_price', y='regression', data=results_df, label='Regression')
    plt.plot([0, results_df['true_price'].max()], [0, results_df['true_price'].max()], 'k--')
    plt.title("Actual vs Predicted")
    
    plt.tight_layout()
    plt.show()