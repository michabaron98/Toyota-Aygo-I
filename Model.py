#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from sklearn.model_selection import train_test_split
#from sklearn.tree import DecisionTreeRegressor
#from sklearn.ensemble import RandomForestRegressor
from numpy import zeros
import re
import xgboost as xgb
import numpy as np
from sklearn.metrics import mean_squared_error as MSE
from sklearn.metrics import accuracy_score
pd.set_option('display.expand_frame_repr', False)
keys=['Saler','Production Year','Milage','Transmition','Quantity of doors',
    'Color', 'Invoice','Country of origin', 'Accident-free','Serviced in aso', 'First registration','Polish registration',
    'First owner','Alloy wheels','Description']
My_toyota=dict(dict(zip(keys, zeros(len(keys)))))
My_toyota={'Saler':'Osoby prywatnej',
    'Production Year':2011,
    'Milage':12000,
    'Transmition':'Manualna',
    'Quantity of doors':5,
    'Color':'Czerwony',
    'Invoice':0,
    'Country of origin':'Niemcy',
    'Accident-free':1,
    'Serviced in aso':0,
    'First registration':"15/06/2020",
    'Polish registration':1,
    'First owner':0,
    'Alloy wheels':1,
    #'price':0,
    #'Description':"",
    'location':1}


# In[2]:


Train_data_path="Cars_details.csv"

# In[3]:


training_file=pd.read_csv(Train_data_path,index_col='Unnamed: 0')
#training_file.drop('', inplace=True)#usunąć pierwsz kolumne
#print(training_file.columns)
# X_features=list(training_file.drop(['Unnamed: 0','price','Description'],axis=1).columns)
# print("X: {}".format(X_features))
# Y_features=['price']
# print("Y: {}".format(Y_features))

#print(training_file.describe().T)
#print(training_file.isnull().sum()/180*100)
#print(training_file.tail(5))
training_file.drop(training_file.index[(training_file['Milage'].isnull())], axis=0, inplace=True)
training_file.drop(labels=['Transmition','Description','First registration'],axis=1,inplace=True)
training_file['Milage']=training_file['Milage'].apply(lambda txt: int("".join(re.findall(r'\d+', txt))))

#My_toyota_df.drop(labels=['Transmition','Description','First registration'],axis=1,inplace=True)

#print(training_file)
df=pd.DataFrame()
df=training_file
#pd.concat([df,My_toyota_df])
#df.append(My_toyota_df, ignore_index=True)
df=pd.get_dummies(df,columns=['Saler'],prefix=['Saler_dummies'])
df=pd.get_dummies(df,columns=['Color'],prefix=['Color_dummies'])
df=pd.get_dummies(df,columns=['Quantity of doors'],prefix=['Quantity of doors_dummies'])
df=pd.get_dummies(df,columns=['Country of origin'],prefix=['Country of origin_dummies'])


# My_toyota_df=pd.get_dummies(My_toyota_df,columns=['Saler'],prefix=['Saler_dummies'])
# My_toyota_df=pd.get_dummies(My_toyota_df,columns=['Color'],prefix=['Color_dummies'])
# My_toyota_df=pd.get_dummies(My_toyota_df,columns=['Quantity of doors'],prefix=['Quantity of doors_dummies'])
# My_toyota_df=pd.get_dummies(My_toyota_df,columns=['Country of origin'],prefix=['Country of origin_dummies'])

Y=df["price"]
X=df.drop(labels=['price'],axis=1)
My_toyota_df=pd.DataFrame(My_toyota,columns=df.columns, index=[0])
My_toyota_df.drop(labels=['price'],axis=1,inplace=True)
My_toyota_df.fillna(0, inplace=True)
#print(My_toyota_df)
#df.drop(df.iloc[:-1], axis=0, inplace=True)
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
scaler.fit(X)
#print("X: {}".format(X))
X = scaler.transform(X)
#print(My_toyota_df.describe())
My_toyota_df = scaler.transform(My_toyota_df)
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.1, random_state=100)
model = xgb.XGBRegressor()
model = xgb.XGBRegressor(n_estimators=1000, max_depth=1, eta=0.01, subsample=0.7, colsample_bytree=0.8)
model.fit(X_train, y_train)
pred = model.predict(My_toyota_df)
print("Price of your Toyota: {} PLN".format(int(pred)))