# -*- coding: utf-8 -*-
"""
"""

!pip install scikit-optimize

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from google.colab import files, drive
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import f1_score, recall_score, accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import plot_roc_curve
from sklearn.model_selection import GridSearchCV
from skopt import BayesSearchCV
from sklearn.decomposition import PCA

drive.mount('/content/drive')

"""#Import do dataset Heart"""

df = pd.read_csv('/content/drive/MyDrive/D1G05/Assignment18/heart.csv')

df.head(10)

"""#Dicionário de Variáveis

Dicionário das variáveis

age: The person's age in years
sex: The person's sex (1 = male, 0 = female)
cp: The chest pain experienced (Value 1: typical angina, Value 2: atypical angina, Value 3: non-anginal pain, Value 4: asymptomatic)
trestbps: The person's resting blood pressure (mm Hg on admission to the hospital)
chol: The person's cholesterol measurement in mg/dl
fbs: The person's fasting blood sugar (> 120 mg/dl, 1 = true; 0 = false)
restecg: Resting electrocardiographic measurement (0 = normal, 1 = having ST-T wave abnormality, 2 = showing probable or definite left ventricular hypertrophy by Estes' criteria)
thalach: The person's maximum heart rate achieved
exang: Exercise induced angina (1 = yes; 0 = no)
oldpeak: ST depression induced by exercise relative to rest ('ST' relates to positions on the ECG plot. See more here)
slope: the slope of the peak exercise ST segment (Value 1: upsloping, Value 2: flat, Value 3: downsloping)
ca: The number of major vessels (0-3)
thal: A blood disorder called thalassemia (3 = normal; 6 = fixed defect; 7 = reversable defect)
target: Heart disease (0 = no, 1 = yes)

#Análise dos Dados
"""

df.isnull().sum()

df = df.drop_duplicates()
df.shape

"""#Análises Gráficas dos Dados

##Análise de correlação entre as features
"""

plt.figure(figsize= (20,10))
a = sns.heatmap(data=df.corr(), annot=True)

"""##Análise do Target"""

sns.countplot(data= df, x='target')

"""##Análise da qte de homens e mulheres com ou sem doença no coração"""

sns.countplot(data=df, x= 'sex', hue='target')

"""##Análise de doença por idade"""

plt.figure(figsize=(20,8))
sns.countplot(data=df, x='age', hue='target')

"""##Tratamento dos dados"""

lista_cat = ['cp','thal','slope','sex','fbs','restecg','exang']
lista_num = ['age', 'trestbps', 'chol', 'thalach', 'oldpeak', 'ca', 'target']

df_geral = pd.get_dummies(df,columns=lista_cat)
df_geral.head()

"""#Normalização das features Numéricas"""

scaler = MinMaxScaler()
df_geral[lista_num] = pd.DataFrame(scaler.fit_transform(df_geral[lista_num].values), columns=lista_num, index=df_geral.index)

df_geral.head()

"""#Separação do DF de Treino e Teste"""

X = df_geral.drop('target', axis=1)
y = df_geral['target']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30)

X_train.shape, X_test.shape, y_train.shape, y_test.shape

"""#Modelagem

## Decision Tree Classifier
"""

dtc = DecisionTreeClassifier()
dtc.fit(X_train, y_train)
y_dtc = dtc.predict(X_test)

print(f'accuracy_score: {accuracy_score(y_test, y_dtc)}')
print(f'f1_score: {f1_score(y_test, y_dtc)}')
print(f'recall_score: {recall_score(y_test, y_dtc)}')

plot_roc_curve(dtc, X_test, y_test)

"""###Hiper Parametrização usando Grid Search"""

param_grid = {
    "criterion": ['gini', 'entropy'],
    "splitter": ['best', 'random'],
    'max_depth': list(range(5))+[None],
    'min_samples_split': list(range(5)),
    'min_samples_leaf': list(range(1,5)),
    'max_features': list(range(2,7)),
    'max_leaf_nodes': list(range(5))
}

dtc = DecisionTreeClassifier()
grid_search = GridSearchCV(dtc,param_grid=param_grid, cv = 5, n_jobs=-1, verbose=2)

grid_search.fit(X_train, y_train)

grid_search.best_params_

best_dtc = grid_search.best_estimator_

y_bdtc = best_dtc.predict(X_test)

print(f'accuracy_score: {accuracy_score(y_test, y_bdtc)}')
print(f'f1_score: {f1_score(y_test, y_bdtc)}')
print(f'recall_score: {recall_score(y_test, y_bdtc)}')
plot_roc_curve(best_dtc, X_test, y_test)

"""###Hiper Parametrização usando Bayes Search"""

param_grid2 = {
    "criterion": ['gini', 'entropy'],
    "splitter": ['best', 'random'],
    'max_depth': list(range(1,5))+[None],
    'min_samples_split': list(range(2,5)),
    'min_samples_leaf': list(range(2,5)),
    'max_features': list(range(2,7)),
    'max_leaf_nodes': list(range(2,5))
}

dtc = DecisionTreeClassifier()
bayes_search = BayesSearchCV(dtc, search_spaces=param_grid2, cv = 5, n_jobs=-1, verbose=2)
bayes_search.fit(X_train, y_train)

bayes_search.best_params_

dtc_bayes = bayes_search.best_estimator_

y_bdtc2 = dtc_bayes.predict(X_test)

print(f'accuracy_score: {accuracy_score(y_test, y_bdtc2)}')
print(f'f1_score: {f1_score(y_test, y_bdtc2)}')
print(f'recall_score: {recall_score(y_test, y_bdtc2)}')
plot_roc_curve(dtc_bayes, X_test, y_test)

"""##Random Forest Classifier"""

rfc = RandomForestClassifier()
rfc.fit(X_train, y_train)
y_rfc = rfc.predict(X_test)

print(f'accuracy_score: {accuracy_score(y_test, y_rfc)}')
print(f'f1_score: {f1_score(y_test, y_rfc)}')
print(f'recall_score: {recall_score(y_test, y_rfc)}')

plot_roc_curve(rfc, X_test, y_test)

"""###Hiper Parametrização Bayes Search"""

rfc_param_grid = {
    'n_estimators': list(range(90,120)),
    "criterion": ['gini', 'entropy'],
    'max_depth': list(range(1,5))+[None],
    'min_samples_split': list(range(2,5)),
    'min_samples_leaf': list(range(1,5)),
    'max_features': list(range(2,7)),
    'max_leaf_nodes': list(range(2,5)),
    'bootstrap': [True, False]
}

rfc = RandomForestClassifier()
bayes_search = BayesSearchCV(rfc, search_spaces=rfc_param_grid, cv = 5, n_jobs=-1, verbose=2)
bayes_search.fit(X_train, y_train)

bayes_search.best_params_
rfc_bayes = bayes_search.best_estimator_
y_brfc = rfc_bayes.predict(X_test)
print(f'accuracy_score: {accuracy_score(y_test, y_brfc)}')
print(f'f1_score: {f1_score(y_test, y_brfc)}')
print(f'recall_score: {recall_score(y_test, y_brfc)}')
plot_roc_curve(rfc_bayes, X_test, y_test)

"""##Naive Bayes Gaussian NB"""

nb = GaussianNB()
nb.fit(X_train, y_train)
y_nb = nb.predict(X_test)

print(f'accuracy_score: {accuracy_score(y_test, y_nb)}')
print(f'f1_score: {f1_score(y_test, y_nb)}')
print(f'recall_score: {recall_score(y_test, y_nb)}')

plot_roc_curve(nb, X_test, y_test)

"""###Hiper Paremetrização Bayes Search"""

nb_param_grid = {
    'var_smoothing': list(np.linspace(0.0000000001,0.00000008,num=11))
}

bayes_search = BayesSearchCV(nb, search_spaces=nb_param_grid, cv = 5, n_jobs=-1, verbose=2)
bayes_search.fit(X_train, y_train)

bayes_search.best_params_
rfc_bayes = bayes_search.best_estimator_
y_bnb = rfc_bayes.predict(X_test)
print(f'accuracy_score: {accuracy_score(y_test, y_bnb)}')
print(f'f1_score: {f1_score(y_test, y_bnb)}')
print(f'recall_score: {recall_score(y_test, y_bnb)}')
plot_roc_curve(rfc_bayes, X_test, y_test)

"""##Gradient Boosting Classifier"""

gbc = GradientBoostingClassifier()
gbc.fit(X_train, y_train)
y_gbc = gbc.predict(X_test)

print(f'accuracy_score: {accuracy_score(y_test, y_gbc)}')
print(f'f1_score: {f1_score(y_test, y_gbc)}')
print(f'recall_score: {recall_score(y_test, y_gbc)}')

plot_roc_curve(gbc, X_test, y_test)

"""###Hiper Parametrização Bayes Search"""

gbc_param_grid = {
    'loss': ['deviance', 'exponential'],
    'learning_rate': list(np.linspace(0.00001,1, num=20)),
    'n_estimators': list(range(90,120)),
    'subsample': list(np.linspace(0.1,1.0,num=10)),
    'criterion': ['friedman_mse', 'mse', 'mae'],
    'min_samples_split': list(range(2,7)),
    'min_samples_leaf': list(range(2,7)),
    'max_depth':list(range(2,7)),
    'max_features':list(range(2,7)),
    'max_leaf_nodes': list(range(2,3))
}

bayes_search = BayesSearchCV(gbc, search_spaces=gbc_param_grid, cv = 5, n_jobs=-1, verbose=2)
bayes_search.fit(X_train, y_train)

bayes_search.best_params_
gbc_bayes = bayes_search.best_estimator_
y_bgbc = gbc_bayes.predict(X_test)
print(f'accuracy_score: {accuracy_score(y_test, y_bgbc)}')
print(f'f1_score: {f1_score(y_test, y_bgbc)}')
print(f'recall_score: {recall_score(y_test, y_bgbc)}')
plot_roc_curve(gbc_bayes, X_test, y_test)

"""##SVC"""

svc = SVC()
svc.fit(X_train, y_train)
y_svc = svc.predict(X_test)

print(f'accuracy_score: {accuracy_score(y_test, y_svc)}')
print(f'f1_score: {f1_score(y_test, y_svc)}')
print(f'recall_score: {recall_score(y_test, y_svc)}')

plot_roc_curve(svc, X_test, y_test)

"""###Hiper Parametrização Bayes Search"""

svc_param_grid = {
    'C': list(range(2,7)),
    'kernel': ['linear','poly','sigmoid'],
    'degree': list(range(1,5)),
    'gamma': ['scale','auto']
}

bayes_search = BayesSearchCV(svc, search_spaces=svc_param_grid, cv = 5, n_jobs=-1, verbose=2)
bayes_search.fit(X_train, y_train)

bayes_search.best_params_
svc_bayes = bayes_search.best_estimator_
y_bsvc = svc_bayes.predict(X_test)
print(f'accuracy_score: {accuracy_score(y_test, y_bsvc)}')
print(f'f1_score: {f1_score(y_test, y_bsvc)}')
print(f'recall_score: {recall_score(y_test, y_bsvc)}')
plot_roc_curve(svc_bayes, X_test, y_test)
