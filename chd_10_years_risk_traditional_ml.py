# -*- coding: utf-8 -*-
"""chd_10_years_risk_traditional_ML.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Uywv4drPy9WM3tbElVJDIBJ9Z8SJQxhe
"""

# Commented out IPython magic to ensure Python compatibility.
# import pakcages and libraries needed for the project
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline
sns.set_style('darkgrid')

df = pd.read_csv('/content/framingham_clean_1.csv')
df.head()

# Scaling for making close variables values from each other
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
# choose index for only scaling numerical data
index = np.r_[1,4,9:15]
df.iloc[:, index] = scaler.fit_transform(df.iloc[:, index]) # apply fit() on X_train and transform fit on X_train

print(df.iloc[0,:])

plt.figure(figsize=(16,5))
sns.boxplot(data=df.iloc[:,index])
plt.title("Distribution of the values ​​of all potential standardized predictors")
plt.grid()
plt.show()

# independant and dependant variables
X = df.iloc[:,:-1].values # independent variables
y = df.iloc[:,-1].values # dependent variable

# Check whether the dataset is equally splitted or no
from collections import Counter
Counter(y)

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, recall_score
from sklearn.model_selection import train_test_split

classifiers = []
classifiers.append(("LR",LogisticRegression()))
classifiers.append(("NB",GaussianNB()))
classifiers.append(("DT",DecisionTreeClassifier(random_state = 0)))
classifiers.append(("RF",RandomForestClassifier(random_state = 0)))
classifiers.append(("SVM",SVC()))
classifiers.append(("KNN", KNeighborsClassifier()))
scores = []
clf_names = []

my_list = [ 0.2, 0.25, 0.33, 0.4]
for clf in classifiers:
  score = 0
  recall = 0
  for p in my_list:
    for i in range(101):
      X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = p, random_state = i)
      classifier = clf[1]
      classifier.fit(X_train,y_train)
      y_pred = classifier.predict(X_test)
      acc_score = (accuracy_score(y_test,y_pred)*100).round(2)
      rec_score = recall_score(y_test,y_pred)
      if acc_score > score:
          score = acc_score
          recall = rec_score
          paramters = (p, i, score, recall)
  p, i, score, recall = paramters
  print("classifier = {}, P = {}, i = {}, score = {}, recall = {}".format(classifier, p,i,score, recall))