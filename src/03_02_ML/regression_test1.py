import numpy as np
from sklearn.linear_model import LinearRegression

# Generate some sample data
x = np.array([1, 2, 3, 4, 5]).reshape((-1, 1))
y = np.array([2, 3, 4, 5, 6])

# Create the model
model = LinearRegression()

# Fit the model to the data
model.fit(x, y)

# Predict the outcome for a new data point
new_x = np.array([6]).reshape((-1, 1))
y_pred = model.predict(new_x)

# Print the coefficients and predicted outcome
print('Coefficients: ', model.coef_)
print('Intercept: ', model.intercept_)
print('Predicted outcome: ', y_pred[0])
