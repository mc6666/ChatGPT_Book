You are a Clean Code expert, I have the following code, please refactor it in a more clean and concise way so that my colleagues can maintain the code more easily. Also, explain why you want to refactor the code so that I can add the explanation to the Pull Request.
[
# 分類(Classification)
import pandas as pd
import numpy as np
from sklearn import datasets

ds = datasets.load_iris()

X=pd.DataFrame(ds.data, columns=ds.feature_names)
y=ds.target

# 資料分割
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)
X_train.shape, X_test.shape, y_train.shape, y_test.shape

# Define and train the KNN model
from sklearn.neighbors import KNeighborsClassifier
clf = KNeighborsClassifier()
clf.fit(X_train, y_train)

# 預測
y_pred = clf.predict(X_test)

# 幫模型打分數
from sklearn.metrics import accuracy_score
print(accuracy_score(y_test, y_pred))
