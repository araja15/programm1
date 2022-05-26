#!/usr/bin/env python
# coding: utf-8

# # Сессия 1
# ---

# In[53]:


# импорт библиотек
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt 

get_ipython().run_line_magic('matplotlib', 'inline')


# ### 1.1 Подготовка данных

# Необходимо выполнить подготовку данных для дальнейшего  анализа и построения прогнозных моделей. Следует выполнить загрузку всех необходимых данных по пассажирским перевозкам. Требуется выполнить объединение двух частей набора данных по перевозкам.

# In[54]:


first_part = pd.read_excel("train_first_part.xlsx")
second_part = pd.read_json("train_second_part.json")
weather = pd.read_csv("weather.csv")


# In[55]:


first_part.head()


# In[56]:


second_part.head()


# Объединяем выборки

# In[57]:


df = pd.concat([first_part, second_part]).drop_duplicates("id").drop("id", axis = 1)


# In[58]:


df


# In[59]:


df.info()


# In[60]:


df["pickup_datetime"] = pd.to_datetime(df["pickup_datetime"])
df["dropoff_datetime"] = pd.to_datetime(df["dropoff_datetime"])

df.info()


# ### Форматирование данных

# In[61]:


plt.figure(figsize = (10, 10))
sns.heatmap(df.isna())


# In[62]:


df.info()


# In[63]:


df["trip_duration"] = df["trip_duration"].apply(lambda x : x / 60)


# In[64]:


df["trip_duration"]


# In[65]:


df.describe()


# In[66]:


import warnings
warnings.filterwarnings("ignore")
plt.figure(figsize = (5 , 5))
sns.boxplot(df["trip_duration"])


# In[67]:


for i in range(90, 101):
    qunt = df["trip_duration"].quantile(i/100)
    df_qunt = df[df["trip_duration"] < qunt]["trip_duration"]
    
    sns.boxplot(df_qunt)
    plt.title(i)
    plt.show()


# In[68]:


q_up = df["trip_duration"].quantile(0.93)
df = df[df["trip_duration"] < q_up]


# In[69]:


df["store_and_fwd_flag"].value_counts()


# In[70]:


d_tm = {"N" : 0, "Y" : 1}
df["store_and_fwd_flag"] = df["store_and_fwd_flag"].map(d_tm)
df["store_and_fwd_flag"].value_counts()


# ## Форматирование погодных данных

# In[71]:


weather.isna().sum()


# In[72]:


for col in ["precipitation", "snow fall", "snow depth"]:
    print(weather[col].unique())
    print("-" * 10)


# In[73]:


for col in ["precipitation", "snow fall", "snow depth"]:
    weather.loc[weather[col] == "T", col] = 0
    weather[col] = weather[col].astype(float)


# In[74]:


weather.describe()


# In[75]:


for temp in ["maximum temperature", "minimum temperature", "average temperature"]:
    weather[temp] = weather[temp].apply(lambda x : (x - 32)/1.8)


# In[76]:


weather.describe()


# In[77]:


df["date"] = df["pickup_datetime"].apply(lambda x : str(x.day) + "-" + str(x.month) + "-" + str(x.year))
df = df.merge(weather, on = "date").drop(["date", "dropoff_datetime"], axis = 1)
df.head()


# # Сохранение данных и вывод о проделанной работе

# In[78]:


print("Сохранение данных!")
df.to_csv("c1_result.csv", index = False)
print("Данные сохранены")


# ### Вывод

# - Обработаны пропуски во всех данных
# - Обработаны выбросы во всех данных
# - данные приведены к приемлемому формату
# - Объединены данные о всех поездаках и о погоде в том числе

# In[ ]:





# In[ ]:




