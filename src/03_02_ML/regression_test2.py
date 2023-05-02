import numpy as np

# Generate some sample data
x = np.array([1, 2, 3, 4, 5])
y = np.array([2, 3, 4, 5, 6])

# Calculate the slope and y-intercept of the regression line
slope, intercept = np.polyfit(x, y, 1)

# Use the slope and y-intercept to make predictions
new_x = 6
y_pred = slope * new_x + intercept

# Print the slope, y-intercept, and predicted outcome
print('Slope: ', slope)
print('Y-intercept: ', intercept)
print('Predicted outcome: ', y_pred)
