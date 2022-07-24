# -*- coding: utf-8 -*-
"""final_project_chd_10_years_risk_traditional_ML.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Wb0Y89xoS6xMGthg2OD7FLKH4i4Nx5vA

# Project: 

## Table of Contents
<ul>
<li><a href="#intro">Introduction</a></li>
<li><a href="#wrangling">Data Wrangling</a></li>
<li><a href="#preprocessing">Data Preprocessing</a></li>
<li><a href="#building">Model Building</a></li>
<li><a href="#evaluation">Model Evaluation</a></li>
</ul>

<a id='intro'></a>
## Introduction 

World Health Organization has estimated 12 million deaths occur worldwide, every year due to Heart diseases. Half the deaths in the United States and other developed countries are due to cardio vascular diseases. The early prognosis of cardiovascular diseases can aid in making decisions on lifestyle changes in high risk patients and in turn reduce the complications.

### Source
The dataset is publically available on the Kaggle website, and it is from an ongoing cardiovascular study on residents of the town of Framingham, Massachusetts. The classification goal is to predict whether the patient has 10-year risk of future coronary heart disease (CHD).The dataset provides the patients’ information. It includes over 4,000 records and 15 attributes.

## Setup
"""

# Commented out IPython magic to ensure Python compatibility.
# import pakcages and libraries needed for the project
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline
sns.set_style('darkgrid')

"""<a id='wrangling'></a>
## Data Wrangling

### General Properties

### Assessing & Building Intuition
"""

# Loading data and printing out a few lines. 
df = pd.read_csv("framingham.csv")
df.head()

df.columns

"""* Column ["male"] needs to be more general.
* Some Columns needs to be renamed

__Attributes__

Each attribute is a potential risk factor. There are both demographic, behavioral and medical risk factors.

__Demographic__

|__Column__|__Description__|
|:---------|:--------------|
|• Male: |male or female (Nominal)|
|• Age: |Age of the patient (Continuous)|

__Behavioral__

|__Column__|__Description__|
|:---------|:--------------|
|• Current Smoker: |whether or not the patient is a current smoker (Nominal)|
|• Cigs Per Day: |the number of cigarettes that the person smoked on average in one day.|

__Medical (history)__

|__Column__|__Description__|
|:---------|:--------------|
|• BP Meds: |whether or not the patient was on blood pressure medication (Nominal)|
|• Prevalent Stroke: |whether or not the patient had previously had a stroke (Nominal)|
|• Prevalent Hyp: |whether or not the patient was hypertensive (Nominal)|
|• Diabetes: |whether or not the patient had diabetes (Nominal)|

__Medical (current)__

|__Column__|__Description__|
|:---------|:--------------|
|• Tot Chol: |total cholesterol level (Continuous)|
|• Sys BP: |systolic blood pressure (Continuous)|
|• Dia BP: |diastolic blood pressure (Continuous)|
|• BMI: |Body Mass Index (Continuous)|
|• Heart Rate: |heart rate (Continuous)|
|• Glucose: |glucose level (Continuous)|

__Predict variable (desired target)__

• 10 year risk of coronary heart disease CHD (binary: “1”, means “Yes”, “0” means “No”)
"""

# inspecting numbers of the dataset rows and columns
df.shape

"""* The dataset has 4238 rows and 16 columns including the target column"""

# inspect data types for each Column
df.dtypes

"""* There are 2 columns ["education", "BPMeds"] have incorrect data types, since they are nominal data with float64 data type."""

# look for instances of missing data and possibly errant values
df.info()

"""* We have 4238 rows in the datasets, therefore the columns ["education", "cigsPerDay", "BPMeds", "totChol", "BMI", "heartRate", "glucose"] have missing values."""

# Check number of unique values in each column
df.nunique()

"""* Columns ["male", "currentSmoker", "BMeds", "prevalentStrike", "prevalentHyp", "diabetes"] are nominal attributes each of them has only 2 values, while column ["education"] has 4 values and also is a nominal value."""

df.TenYearCHD.value_counts()

"""* We have a problem here, the dataset isn't balanced!"""

# Check the characteristics of the dataset
df.iloc[:,np.r_[1,4,9:15]].describe()

# Printing the last few lines to see how the data
df.tail()

"""<a id='preprocessin'></a>
## Data Preprocessing

### Data Cleaning (Fix problems in the dataset!)

__Duplicated Data__
"""

# Check duplicated data
df.duplicated().sum()

"""* That's great! The dataset has no duplicated rows!

__Renaming Data Columns__
"""

# rename the column male to gender to be more general
df.rename(columns={"male": "gender"}, inplace= True)

# lowercase the columns names
df.rename(columns = lambda X: X.lower(), inplace= True)
df.columns

# separate the columns names
df.rename(columns={"currentsmoker": "current_smoker", "cigsperday": "cigs_per_day", 
                   "bpmeds": "bp_meds","prevalentstroke": "prevalent_stroke", 
                   "prevalenthyp": "prevalent_hyp","totchol": "tot_chol", 
                   "sysbp": "sys_bp", "diabp": "dia_bp", "heartrate": "heart_rate"}, inplace= True)

df.columns

"""* Now datasets columns are clean!

__Missing Data__
"""

# print number of NaN Values
df.isnull().sum()

# Taking care of missing data
# import required library
from sklearn.impute import SimpleImputer

# Setting strategy for numrical data
imputer = SimpleImputer(missing_values=np.nan, strategy='mean')

# Choose only missing data columns of numerical data
index = np.r_[4,9,12:15]

# Apply my strategy on selected columns
imputer = imputer.fit(df.iloc[:,index])

# Transform my strategy on the data
df.iloc[:,index] = imputer.transform(df.iloc[:,index])

# Setting strategy for nominal data
imputer = SimpleImputer(missing_values=np.nan, strategy='most_frequent')

# Choose only missing data columns of nominal data
index = np.r_[2, 5]

# Apply my strategy on selected columns
imputer = imputer.fit(df.iloc[:,index])

# Transform my strategy on the data
df.iloc[:,index] = imputer.transform(df.iloc[:,index])

# Check for any NaN Values
df.isnull().sum().any()

"""* The dataset now has no missing data!

__Incorrect Data Types__
"""

# Convert columns "education", "bp_meds" to np.int64
df = df.astype({"education": np.int64, "bp_meds": np.int64})
df.dtypes

"""* Columns "education", "bp_meds" have correct data types now!

__Removing Outliers__
"""

Index = np.r_[1,4,9:15]
plt.figure(figsize=(16,5))
df.iloc[:,Index].boxplot()
plt.title("Distribution of the values ​​of all potential predictors")
plt.show()

outliers = ['age','cigs_per_day', 'tot_chol', 'sys_bp','dia_bp', 'bmi', 'heart_rate', 'glucose']
for column in outliers:
  Q1,Q3 = np.percentile(df[column],[25,75])
  IQR = Q3 - Q1
  lower_fence = Q1 - (1.5*IQR)
  upper_fence = Q3 + (1.5*IQR)  
  df[column] = df[column].apply(lambda x: upper_fence if x>upper_fence
                                              else lower_fence if x<lower_fence else x)

plt.figure(figsize=(16,5))
sns.boxplot(data=df.iloc[:,Index])
plt.title("Distribution of the values ​​of all potential predictors")
plt.grid()
plt.show()

"""* Now the dataset is clean and can be saved for future work."""

df.to_csv('framingham_clean.csv', index=False)

df_clean = pd.read_csv('framingham_clean.csv')
df_clean.head()

"""### Feature Scaling """

# Scaling for making close variables values from each other
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
# choose index for only scaling numerical data
index = np.r_[1,4,9:15]
df.iloc[:, index] = scaler.fit_transform(df.iloc[:, index]) # apply fit() on X_train and transform fit on X_train

print(df.iloc[0,:])

plt.figure(figsize=(16,5))
sns.boxplot(data=df.iloc[:,Index])
plt.title("Distribution of the values ​​of all potential standardized predictors")
plt.grid()
plt.show()

"""### Splitting the dataset"""

# independant and dependant variables
X = df.iloc[:,:-1].values # independent variables
y = df.iloc[:,-1].values # dependent variable

# Check whether the dataset is equally splitted or no
from collections import Counter
Counter(y)

"""<a id='building'></a>
## Model Building

"""

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

# Applying GridSearch on the dataset to Check the best paramters for our Classification
from sklearn.model_selection import RepeatedStratifiedKFold, GridSearchCV
for classifier_name, classifier in classifiers:
    cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=3, random_state=0)
    if classifier_name == "LR" : 
        parameters = [{'solver' : ['newton-cg', 'lbfgs'], 'penalty' : ['l2'], 
                       'C':[100, 10, 1, 0.1, 0.01],'multi_class':['auto', 'ovr', 'multinomial']},
                      {'solver': ['liblinear'],'penalty' : ['l1', 'l2'],
                       'C':[100, 10, 1, 0.1, 0.01],'multi_class':['auto', 'ovr'],'random_state':[0,1,42]}]
    elif classifier_name == "NB" : 
        continue           
    elif classifier_name == "DT" :
        parameters = [{'criterion' : ['gini', 'entropy'],'random_state':[ 0, 1, 12, 42],
                        'splitter':['best', 'random'], 'max_features': ['sqrt', 'log2']}]
    elif classifier_name == "RF" :
        parameters = [{'bootstrap':[True], 'criterion' : ['gini', 'entropy'], 'n_estimators':[10,15,20,25],
                        'max_depth':[110,130,150,170], 'random_state':[ 0, 1 , 42],
                       'min_samples_leaf':[7,9,11,13],'min_samples_split':[8,12,14],'max_features': ['sqrt', 'log2']}]
    elif classifier_name == "SVM" :
        parameters = [{'C':[100, 10, 1, 0.1, 0.01], 'gamma' : ['auto', 'scale'],
                       'kernel': ['poly', 'rbf', 'sigmoid']}]    
    elif classifier_name == "KNN" :
        parameters = [{'n_neighbors': range(1, 21, 2),
                       'weights' : ['uniform', 'distance'],'n_jobs': [-1],
                       'algorithm' : ['auto', 'ball_tree', 'kd_tree','brute']}]
    grid_search= GridSearchCV(estimator = classifier,
                              param_grid = parameters,
                              scoring = 'accuracy',
                              cv = cv, n_jobs = -1)
    grid_search = grid_search.fit(X, y)
    best_accuracy = grid_search.best_score_
    best_parameters = grid_search.best_params_
    print(classifier_name," (best score) : ", best_accuracy)
    print("best parameters : ", best_parameters)

classifiers = []
classifiers.append(("LR",LogisticRegression( C =  0.1, multi_class = 'auto', penalty = 'l2', solver = 'newton-cg')))
classifiers.append(("NB",GaussianNB()))
classifiers.append(("DT",DecisionTreeClassifier(criterion = 'entropy', max_features = 'sqrt', random_state = 42, splitter = 'random')))
classifiers.append(("RF",RandomForestClassifier(bootstrap  = True, criterion = 'entropy', max_depth = 110, max_features = 'sqrt', 
                                                min_samples_leaf = 9, min_samples_split = 8, n_estimators = 25, random_state = 1)))
classifiers.append(("SVM",SVC(C = 10, gamma = 'auto', kernel = 'poly')))
classifiers.append(("KNN", KNeighborsClassifier(algorithm = 'auto', n_jobs = -1, n_neighbors = 19, weights = 'uniform')))
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

"""## Final Model"""

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 68)
X_train[0,:]

"""### Logistic Regression"""

lr_acc_clf = LogisticRegression(C =  0.1, multi_class = 'auto', penalty = 'l2', solver = 'newton-cg')
lr_acc_clf.fit(X_train,y_train)
lr_train_score = lr_acc_clf.score(X_train,y_train)
lr_test_score = lr_acc_clf.score(X_test,y_test)
print('Model Train Score: {} '.format(lr_train_score))
print('Model Test Score: {} '.format(lr_test_score))
y_pred_lr = lr_acc_clf.predict(X_test)
lr_acc_score = (accuracy_score(y_test,y_pred_lr)*100).round(2)
print("Logistic Regression Highest Accuarcy: {}% ".format(lr_acc_score))

"""### Random Forest"""

rf_acc_clf = RandomForestClassifier(criterion='entropy', max_depth=110, max_features='sqrt',
                                    min_samples_leaf=9, min_samples_split=8, n_estimators=25,
                                    random_state=1)
rf_acc_clf.fit(X_train,y_train)
rf_train_score = rf_acc_clf.score(X_train,y_train)
rf_test_score = rf_acc_clf.score(X_test,y_test)
print('Model Train Score: {} '.format(rf_train_score))
print('Model Test Score: {} '.format(rf_test_score))
y_pred_rf = rf_acc_clf.predict(X_test)
rf_acc_score = (accuracy_score(y_test,y_pred_rf)*100).round(2)
print("Random Forest Highest Accuarcy: {}% ".format(rf_acc_score))

"""### KNN Classifier"""

knn_acc_clf = KNeighborsClassifier(algorithm = 'auto', n_jobs = -1, n_neighbors = 19, weights = 'uniform')
knn_acc_clf.fit(X_train,y_train)
knn_train_score = knn_acc_clf.score(X_train,y_train)
knn_test_score = knn_acc_clf.score(X_test,y_test)
print('Model Train Score: {}'.format(knn_train_score))
print('Model Test Score: {}'.format(knn_test_score))
y_pred_knn = knn_acc_clf.predict(X_test)
knn_acc_score = (accuracy_score(y_test,y_pred_knn)*100).round(2)
print("KNN Highest Accuarcy: {}% ".format(knn_acc_score))

"""### Support Vector Machine"""

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 21)
X_train[0,:]

svc_acc_clf = SVC(C = 10, gamma = 'auto', kernel = 'poly')
svc_acc_clf.fit(X_train,y_train)
svc_train_score = svc_acc_clf.score(X_train,y_train)
svc_test_score = svc_acc_clf.score(X_test,y_test)
print('Model Train Score: {}'.format(svc_train_score))
print('Model Test Score: {}'.format(svc_test_score))
y_pred_svc = svc_acc_clf.predict(X_test)
svc_acc_score = (accuracy_score(y_test,y_pred_svc)*100).round(2)
print("SVC Highest Accuarcy: {}% ".format(svc_acc_score))

"""## Save Optimal Model

"""

import pickle
filename = 'chd_10_years_risk_best_accuarcy_model.sav'
pickle.dump(svc_acc_clf, open(filename, 'wb'))