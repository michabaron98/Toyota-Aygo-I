#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor


# In[ ]:





# In[2]:


Train_data_path="Toyota_aygo_I.csv"


# In[3]:


training_file=pd.read_csv(Train_data_path)


# In[4]:


Y_training=training_file[["price"]].round(decimals=-2)
Features_X=[]
X_training_1=training_file[["year","location"]]
print(X_training_1)
X_training_mileage=pd.DataFrame(training_file[["mileage"]].round(decimals=-3),columns=['mileage'])
X_training=X_training_1.join(X_training_mileage)
#X_training=X_training.join(training_file["location"])
X_training


# In[5]:


Y_training.describe()


# In[6]:


X_training.describe()


# In[11]:


model=RandomForestRegressor(n_estimators=100, oob_score=True, random_state=16)
model.fit(X_training, Y_training)
predictions=model.predict(X_training)


# In[12]:


moja_toyota=[]
moja_toyota.append([2011,1,117300])
moja_toyota_df=pd.DataFrame(moja_toyota, columns=["year","mileage","location"])
predictions=model.predict(moja_toyota_df)
print("Price: {} PLN".format(int(predictions)))





