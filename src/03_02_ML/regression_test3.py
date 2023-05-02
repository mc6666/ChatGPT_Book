import numpy as np

# Generate some sample data
x = np.array([1, 2, 3, 4, 5])
y = np.array([2, 3, 4, 5, 6])

# Calculate the coefficients of the regression line
X = np.vstack([x, np.ones(len(x))]).T
coeffs = np.linalg.inv(X.T @ X) @ X.T @ y

# Use the coefficients to make predictions
new_x = 6
y_pred = coeffs[0] * new_x + coeffs[1]

# Print the coefficients and predicted outcome
print('Coefficients: ', coeffs)
print('Predicted outcome: ', y_pred)
