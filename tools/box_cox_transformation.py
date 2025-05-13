import numpy as np
from scipy import stats

# Example data
data = np.random.exponential(scale=2.0, size=1000)  # Skewed data

# Apply Box-Cox
transformed_data, best_lambda = stats.boxcox(data)

print(f"Best lambda: {best_lambda}")