#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import time
import json
import numpy as np
import pandas as pd
from pandas import json_normalize
import matplotlib.pyplot as plt
import json
import ast
import scipy.stats as stats


# In[ ]:


test = pd.read_csv('./pre_processed.csv')


# In[24]:


test.shape


# In[ ]:


def load_df(csv_path, nrows = None):
    json_cols = ['device', 'geoNetwork', 'totals', 'trafficSource']
    df = pd.read_csv(csv_path,
                     #converters are dict of functions for converting values in certain columns. Keys can either be integers or column labels.
                     #json.loads() method can be used to parse a valid JSON string and convert it into a Python Dictionary.
                     #It is mainly used for deserializing native string, byte, or byte array which consists of JSON data into Python Dictionary.
                     converters = {col: json.loads for col in json_cols},                                                                         
                         dtype = {'fullVisitorId': 'str'}, # Important!!
                         nrows = nrows)
    for col in json_cols:
        # for each column, flatten data frame such that the values of a single col are spread in different cols
        # This will use subcol as names of flat_col.columns
        flat_col = json_normalize(df[col])
        # Name the columns in this flatten data frame as col.subcol for tracability
        flat_col.columns = [f"{col}.{subcol}" for subcol in flat_col.columns]
        # Drop the json_col and instead add the new flat_col
        df = df.drop(col, axis = 1).merge(flat_col, right_index = True, left_index = True)
    return df


csv_test_path = './test_v2.csv'
test = load_df(csv_test_path, nrows = None)


# In[ ]:


test.shape


# In[ ]:


# Identify non opearting countries 
lowCountries=[]
hitWithCountry = {}
sum = 0
cnt = test['geoNetwork.country'].value_counts(sort=True)
print(cnt)
for i in range(0, cnt.size):
    sum = sum + cnt[i]

#Identify the Non Operating Countries

for i in range(0, cnt.size):
    #print(f"Country Name: {cnt.index[i]} Frequency: {(cnt[i]/sum)*100}%" )
    if((cnt[i]/sum)*100 < 0.01):
        lowCountries.append(cnt.index[i]) 
len(lowCountries)


# In[ ]:


#Data Exploration for Rule 1
#categories = df['Predictions'].to_numpy()
colormap = np.array(['g', 'r'])
hits1 = {}
test['totals.hits'] = pd.to_numeric(test['totals.hits'])
for indx in range(test.index.start, test.index.stop):
    #print(indx)
    country = test.at[indx, 'geoNetwork.country']
    oneIndex = (test.at[indx,'hits'])
    #hitsInfo = ast.literal_eval(oneIndex)
    #print(hitsInfo)
    if country in lowCountries:
        if country not in hits1.keys():
            hits1[country] = (test.at[indx, 'totals.hits'])
        elif country in hits1.keys():
            hits1[country] = hits1[country] + (test.at[indx, 'totals.hits'])
len(hits1)
f = plt.figure(figsize=(12, 4))
f = plt.scatter(hits1.keys(), hits1.values())
f = plt.xlabel('country')
f = plt.ylabel('Total Hits')
f = plt.xticks(rotation=90)
plt.show()


# In[ ]:


##First Rule : If total hits of a session from NON Opearting/rare countries is outlier means 1.5 IQR from Q3
cnt=0
sum=0
lowCountries=[]
hitWithCountry = {}
cnt = test['geoNetwork.country'].value_counts(sort=True)

for i in range(0, cnt.size):
    sum = sum + cnt[i]

#Identify the Non Operating Countries

for i in range(0, cnt.size):
    #print(f"Country Name: {cnt.index[i]} Frequency: {(cnt[i]/sum)*100}%" )
    if((cnt[i]/sum)*100 < 0.01):
        lowCountries.append(cnt.index[i]) 
    

inputCountries = test.at[0,'geoNetwork.country']

test['totals.hits'] = pd.to_numeric(test['totals.hits'])
data = test['totals.hits']
np.median(data)
upper_q = np.percentile(data, 75)
lower_q = np.percentile(data, 25)
iqr = upper_q - lower_q
upper_whisker = data[data<=upper_q+1.5*iqr].max()
lower_whisker = data[data>=lower_q-1.5*iqr].min()
#print(upper_whisker)

for indx in range(test.index.start, test.index.stop):
    #print(indx)
    country = test.at[indx, 'geoNetwork.country']
    oneIndex = (test.at[indx,'hits'])
    #hitsInfo = ast.literal_eval(oneIndex)
    #print(hitsInfo)
    if country in lowCountries:
        hit = test.at[indx, 'totals.hits']
        if int(hit) > upper_whisker:
            test.loc[indx, 'isAnomaly'] = 1
#            print(f"Index Number : {indx} Anomalous traffic Info: {country} Total Hits : {int(hit)} Visit Date:{test.at[indx, 'date']}")
#             for ind in range(0, len(hitsInfo)):
#                 print(f"Hit Number: {hitsInfo[ind]['hitNumber']} Visited Page: {hitsInfo[ind]['appInfo']['screenName']} Keyword: {test.at[indx, 'trafficSource.keyword']}")
        #print(f"Country Name: {country} --> Total hits: {hit}")
#         if country in hitWithCountry.keys():
#             hitWithCountry[country] += 1
#         else:
#             hitWithCountry[country]=1

#newArr = test['hits'].to_numpy()


# In[ ]:


oneIndex = (test.at[0,'hits'])
result = ast.literal_eval(oneIndex)
#print(type(result))
for ind in range(0, len(result)):
    print(f"Hit Number: {result[ind]['hitNumber']} Visited Page: {result[ind]['appInfo']['screenName']}")


# In[ ]:


#Data Exploration for Rule 2
#categories = df['Predictions'].to_numpy()
colormap = np.array(['g', 'r'])
views1 = {}
test['totals.pageviews'] = pd.to_numeric(test['totals.pageviews'])
for indx in range(test.index.start, test.index.stop):
    #print(indx)
    country = test.at[indx, 'geoNetwork.country']
    #oneIndex = (test.at[indx,'totals.pageviews'])
    #hitsInfo = ast.literal_eval(oneIndex)
    #print(hitsInfo)
    if country in lowCountries:
        if country not in views1.keys():
            views1[country] = (test.at[indx, 'totals.pageviews'])
        elif country in views1.keys():
            views1[country] = views1[country] + (test.at[indx, 'totals.hits'])
len(views1)
f = plt.figure(figsize=(12, 4))
f = plt.scatter(views1.keys(), views1.values())
f = plt.xlabel('country')
f = plt.ylabel('Total PageViews')
f = plt.xticks(rotation=90)
plt.show()


# In[ ]:


##Rule 2 : if total pageViews from a session is absurdly higher from RareCountries
sum = 0
test['totals.pageviews'] = pd.to_numeric(test['totals.pageviews'])
##Replace NaN Values with Zero
test['totals.pageviews'].fillna(value = 0, inplace = True)
data = test['totals.pageviews']
upper_q = np.percentile(data, 75)
lower_q = np.percentile(data, 25)
iqr = upper_q - lower_q
upper_whisker = data[data<=upper_q+1.5*iqr].max()
lower_whisker = data[data>=lower_q-1.5*iqr].min()
lower_whisker

## Rule based on the Total PageView
for ind in range(len(test)):
    pageView = test.at[ind , 'totals.pageviews']
    country = test.at[ind , 'geoNetwork.country']
    if pageView > upper_whisker and country in lowCountries:
        test.loc[i, 'isAnomaly'] = 1


# In[ ]:


#Data Exploration for Rule 3
#categories = df['Predictions'].to_numpy()
colormap = np.array(['g', 'r'])

f = plt.figure(figsize=(12, 4))
f = plt.scatter(test['geoNetwork.country'], test['totals.pageviews'])
f = plt.xlabel('country')
f = plt.ylabel('Total PageViews')
f = plt.xticks(rotation=90)
plt.show()


# In[ ]:


##Rule 3 : if total pageViews from a session is absurdly higher from any Country
sum = 0

data = test['totals.pageviews']
upper_q = np.percentile(data, 75)
lower_q = np.percentile(data, 25)
iqr = upper_q - lower_q
upper_whisker = data[data<=upper_q+1.5*iqr].max()
lower_whisker = data[data>=lower_q-1.5*iqr].min()
lower_whisker

## Rule based on the Total PageView
for i in range(len(test)):
    pageView = test.loc[i , 'totals.pageviews']
    country = test.loc[i , 'geoNetwork.country']
    if pageView > upper_whisker*10:
        test.loc[i, 'isAnomaly'] = 1


# In[ ]:


data = test['totals.pageviews']
plt.hist(data)
plt.show()


# In[ ]:


for i,j in zip(test.fullVisitorId.duplicated().index, test.fullVisitorId.duplicated()):
    if j == True:
        print(test.loc[i, 'fullVisitorId'])


# In[ ]:


sum = 0
test['totals.hits'] = pd.to_numeric(test['totals.hits'])
mean = test['totals.hits'].mean()
std = test['totals.hits'].std()
maximum = test['totals.hits'].max()

#plt.boxplot(test['totals.hits'])
#plt.xlim(xmin=0, xmax = 501)
#plt.show()
data = test['totals.hits']
np.median(data)
upper_q = np.percentile(data, 75)
lower_q = np.percentile(data, 25)
iqr = upper_q - lower_q
upper_whisker = data[data<=upper_q+1.5*iqr].max()
lower_whisker = data[data>=lower_q-1.5*iqr].min()
upper_whisker
data    


# In[ ]:


#Data Exploration for Rule 4
#categories = df['Predictions'].to_numpy()
colormap = np.array(['g', 'r'])
tos1 = {}
test['totals.timeOnSite'] = pd.to_numeric(test['totals.timeOnSite'])
for indx in range(test.index.start, test.index.stop):
    #print(indx)
    country = test.at[indx, 'geoNetwork.country']
    #oneIndex = (test.at[indx,'totals.pageviews'])
    #hitsInfo = ast.literal_eval(oneIndex)
    #print(hitsInfo)
    if country in lowCountries:
        if country not in tos1.keys():
            tos1[country] = (test.at[indx, 'totals.pageviews'])
        elif country in tos1.keys():
            tos1[country] = tos1[country] + (test.at[indx, 'totals.hits'])
len(tos1)
f = plt.figure(figsize=(12, 4))
f = plt.scatter(tos1.keys(), tos1.values())
f = plt.xlabel('country')
f = plt.ylabel('Session Duration')
f = plt.xticks(rotation=90)
plt.show()


# In[ ]:


# Rule 4: Session duration is outlier for non operating countries
## total.timeOnSite means session duration of a session
sum = 0
test['totals.timeOnSite'] = pd.to_numeric(test['totals.timeOnSite'])
test['totals.timeOnSite'].fillna(value = 0, inplace = True)
data = test['totals.timeOnSite']
upper_q = np.percentile(data, 75)
lower_q = np.percentile(data, 25)
iqr = upper_q - lower_q
upper_whisker = data[data<=upper_q+1.5*iqr].max()
lower_whisker = data[data>=lower_q-1.5*iqr].min()
for i in range(len(test)):
    timeOnSite = test.at[i, 'totals.timeOnSite']
    country = test.at[i, 'geoNetwork.country']
    if timeOnSite > upper_whisker and country in lowCountries:
        test.loc[i, 'isAnomaly'] = 1


# In[ ]:


# Determining how many users come to our system in an hour to create a baseline for rule 5
#test['visitStartTime'] = pd.to_datetime(test['visitStartTime'], unit='s')
usersWithDate = {}
test['date'] = pd.to_numeric(test['date'])
test = test.sort_values(by = 'visitStartTime')
test = test.reset_index(drop = True)
#print(test)
timeDiff = test['visitStartTime'].max() - test['visitStartTime'].min()
dayDiff = timeDiff / 86400
dayDiff = dayDiff.round()
print(dayDiff)
UsersPerDay = (test['fullVisitorId'].count() / dayDiff).round()
UsersPerHour = (UsersPerDay/24).round()
hourCount = 86400/24
startTime = test.loc[0 , 'visitStartTime']
sumOfUsers = 0
userCounts=[]
for itr in range(len(test)):
    #print(test.loc[itr, 'visitStartTime'])
    if(test.loc[itr, 'visitStartTime'] > (startTime + 3600)):
        startTime = test.loc[itr, 'visitStartTime']
        usersWithDate[startTime] = sumOfUsers
        userCounts.append(sumOfUsers)
        sumOfUsers = 0
    sumOfUsers = sumOfUsers+1
len(userCounts)
#test.head()


# In[ ]:


a = np.array(userCounts)
plt.boxplot(a)
plt.show()


# In[ ]:


#categories = df['Predictions'].to_numpy()
colormap = np.array(['g', 'r'])

f = plt.figure(figsize=(12, 4))
f = plt.scatter(usersWithDate.keys(), usersWithDate.values())
f = plt.xlabel('date')
f = plt.ylabel('usersHour')
f = plt.xticks(rotation=90)
plt.show()


# In[ ]:


# rule 5 : Detect Anomalous users generating higher volume of traffic in an hour
sum = 0
anomalousHours = []
times = {}
data = list(usersWithDate.values())
upper_q = np.percentile(data, 75)
lower_q = np.percentile(data, 25)
iqr = upper_q - lower_q
upper_whisker = upper_q+1.5*iqr
lower_whisker = lower_q-1.5*iqr
for i,j in usersWithDate.items():
    if j > upper_whisker:
        anomalousHours.append(i)

for i in range(len(anomalousHours)):
    for j in range(len(test)):
        endTime = anomalousHours[i]
        startTime = endTime - 3600
        if test.loc[j, 'visitStartTime'] >=startTime and test.loc[j, 'visitStartTime'] <= endTime:
            if j not in times:
                times[j] = (test.loc[j, 'totals.hits'])
            elif j not in times:
                times[j] = times[j] + (test.loc[j, 'totals.hits'])
    data = list(times.values())
    upper_q = np.percentile(data, 75)
    lower_q = np.percentile(data, 25)
    iqr = upper_q - lower_q
    upper_whisker = upper_q+1.5*iqr
    lower_whisker = lower_q-1.5*iqr
#     print(upper_whisker)
    for a, b in times.items():
        if b > upper_whisker:
            test.loc[a, 'isAnomaly'] = 1

#sum
        
    
    


# In[25]:


test['isAnomaly'].fillna(value = 0, inplace = True)
aomalousSessions = test[test['isAnomaly'] == 1]
len(aomalousSessions)


# In[26]:


aomalousSessions.to_csv('./out.csv')  


# In[34]:


kw = test[test['trafficSource.keyword'] != '(not set)']
kw = kw[kw['trafficSource.keyword'] != 'NaN']
kw = kw[kw['trafficSource.keyword'] != '(not provided)']
kw.head()


# In[ ]:




