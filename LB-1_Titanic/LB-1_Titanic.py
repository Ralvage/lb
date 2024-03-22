import numpy as np
import pandas as pd

from matplotlib import pyplot as plt
import seaborn as sns
import os

path_to_train = '/kaggle/input/titanic-machine-learning-from-disaster/train.csv'
path_to_test = '/kaggle/input/titanic-machine-learning-from-disaster/test.csv'
Train = pd.read_csv(path_to_train, index_col = 'PassengerId')
Test = pd.read_csv(path_to_test, index_col = 'PassengerId')
Train
Train.head(5)
Train.tail()
Train[(Train['Age'] == 14)]
Train[(Train['Sex'] == 'male') & (Train['Embarked'] == 'C')]
Train.query("Sex == 'male' & Embarked == 'C'")
Train.info()
Test.info()

def impute_data(df):
    df_copy = df.copy()
    categorial_vars = list(df_copy.select_dtypes(include=['object']).columns.values)
    for col in categorial_vars:
        if(df_copy[col].isnull().values.any()):
            df_copy[col].fillna(df_copy[col].mode()[0],inplace=True)      
    numerical_vars = list(df_copy.select_dtypes(include=['int64', 'float64']).columns.values)
    for col in numerical_vars:
        if(df_copy[col].isnull().values.any()):
            df_copy[col].fillna(df_copy[col].mode()[0],inplace=True)      
    
    return df_copy

train_full = impute_data(Train)
test_full = impute_data(Test)

train_full.info()

train_full['Family_size'] = train_full['Parch'] + train_full['SibSp']
test_full['Family_size'] = test_full['Parch'] + test_full['SibSp']

train_full.head()

(test_full['Sex'] == 'male')
(test_full['Sex'] == 'male') & (test_full['Pclass'] == 3)
simple_pred = (~((test_full['Sex'] == 'male') & (test_full['Pclass'] == 3))).astype(int).values

def make_prediction_file(prediction, test_data, name):
    result = pd.DataFrame({'PassengerId': test_data.reset_index()['PassengerId'], 'Survived': prediction})
    result.to_csv(name, index=False)
    
make_prediction_file(simple_pred, Test, '/kaggle/working/titanic.csv')
