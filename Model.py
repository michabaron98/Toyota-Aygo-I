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
X_training_year=training_file[["year"]]
X_training_mileage=pd.DataFrame(training_file[["mileage"]].round(decimals=-3),columns=['mileage'])
X_training=X_training_year.join(X_training_mileage)


# In[5]:


Y_training.describe()


# In[6]:


X_training.describe()


# In[7]:


model=RandomForestRegressor(n_estimators=100, oob_score=True, random_state=42)
model.fit(X_training, Y_training)
predictions=model.predict(X_training)


# In[12]:


moja_toyota=[]
moja_toyota.append([2011,117300])
moja_toyota_df=pd.DataFrame(moja_toyota, columns=["year","mileage"])
predictions=model.predict(moja_toyota_df)
print("Price: ", predictions)


# In[ ]:




