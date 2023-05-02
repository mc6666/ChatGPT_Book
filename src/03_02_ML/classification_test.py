# Import necessary libraries
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# Load dataset
iris = datasets.load_iris()

# Prepare data
X = iris.data[:, :2]  # We only take the first two features
y = iris.target

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Create SVM classifier object
svm = SVC(kernel='linear')

# Train SVM classifier
svm.fit(X_train, y_train)

# Predict target values for test data
y_pred = svm.predict(X_test)

# Evaluate accuracy of SVM classifier
accuracy = accuracy_score(y_test, y_pred)

print('Accuracy of SVM classifier: {:.2f}'.format(accuracy))
