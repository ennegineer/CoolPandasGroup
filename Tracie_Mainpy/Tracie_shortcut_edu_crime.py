#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies
import numpy as np
import json
import pandas as pd
import matplotlib.pyplot as plt
import requests
import scipy.stats as st
from scipy.stats import linregress
from sklearn import datasets
from pprint import pprint
from config import crimekey
from config import censuskey
from census import Census

c = Census(censuskey, year=2013)


# In[2]:


# Set the file path
edupath = "Resources/cc_institution_details_clean.csv"

# Read the file 
edu = pd.read_csv(edupath,encoding='utf-8')
#crime = pd.read_csv(crimepath)

edu.head()


# In[3]:


edu_df = edu[["state","level","basic","level","student_count"]]
edu_df.head()


# In[4]:


# open population file by reading this file: census_pd.to_csv("Output/census_raw.csv")
# set the path 
Population_path = "Output/census_raw.csv"

# Read the csv file 
Populationdf = pd.read_csv(Population_path)
Populationdf.head()


# In[5]:


# open edu_rate_df by reading csv file : edu_rate_df.to_csv("Output/edu_rate_df.csv", index=False, header=True)
# set the path 
Edu_rate_path = "Output/edu_rate_df.csv"

# Read the csv file 
edu_rate_df = pd.read_csv(Edu_rate_path)
edu_rate_df = edu_rate_df.rename(columns = {"% graduate":"graduate ratio (%)"})
edu_rate_df = edu_rate_df.rename(columns = {"state":"State Name"})
edu_rate_df.head()


# In[6]:


# double check edu df type
edu_rate_df.dtypes


# In[7]:


# groupby edu file by state in order to have common and equal state column to merge later
edu_rate = edu_rate_df.groupby("State Name")["number of graduates","Population","graduate ratio (%)"].mean()
#edu_rate = edu_rate_df.mean()
edu_rate = edu_rate.dropna()
edu_rate.head()


# In[8]:


#open crime report by reading csv file: statemerge.to_csv("Output/statemerge.csv", index=False, header=True)

# set the path 
crime_rate_path = "Data/censuscrimedata.csv"

# Read the csv file 
crime_rate = pd.read_csv(crime_rate_path)
crime_rate.head()


# In[9]:


# extract crime rate per state
crime_rate_df = crime_rate[["State Name","Crime Rate"]]
crime_rate_df["Crime Rate %"] = crime_rate["Crime Rate"]*100
crime_rate_df.head()


# In[10]:


# merge two df together to get master_plot_df
master_plot_df = pd.merge(crime_rate_df, edu_rate, on = "State Name", how = "outer")
master_plot_df["graduate ratio (%)"]=master_plot_df["graduate ratio (%)"]*1000
master_plot_df.head()


# In[11]:


# extract above biggest 10 states to a new master_df to do analysis by conditional with .loc
masterdf = master_plot_df.loc[(master_plot_df["Population"]>=9651300)]
masterdf.head(10)


# In[12]:


# get top 10 big states to do plotting | analysis | #opt: master_plot_df.nlargest(10,"Population") to get the top 10 largest population
#master = master_plot_df.sort_values("Population",ascending=False)
#master.head(10)


# In[13]:


# PLOTTING JOBS 


# In[14]:


# use the masterdf df to implement bar chart to show the crime rates of all states in the US

#define the x and y axis by create a state_list and actuals_list from those columns
x_states = masterdf["State Name"]
y_crime = masterdf["Crime Rate %"]

plt.bar(x_states, y_crime, color='blue', alpha=0.5, align="center")
plt.xticks(rotation="vertical")
plt.title("Top 10 States with crime rates 2019")
plt.xlabel("State Names")
plt.ylabel("Crime Rates")
plt.figure(figsize=(10,200))
plt.savefig("Output/Crime_per_state.png")
plt.show()


# In[15]:


# same df to show the 4-year-academic-graduate ratio from Top 5 states
x_states = masterdf["State Name"]
y_graduate = masterdf["graduate ratio (%)"]
plt.bar(x_states, y_graduate, color='r', alpha=0.5, align="center")
plt.xticks(rotation="vertical")
plt.title("Top 10 States with 4-year-graduate ratio")
plt.xlabel("States")
plt.ylabel("Graduate ratio (%)")
plt.figure(figsize=(10,200))
plt.savefig("Output/Education_states.png")
plt.show()


# In[16]:


# find the correlation bt. education (College graduation rate per population) and crime rate
# do scatter plot first

plt.scatter(masterdf.iloc[:,2],masterdf.iloc[:,5],marker="o", facecolors="red", edgecolors="black")
plt.xlabel('4-year-college Graduate Ratio 2019')
plt.ylabel('Crime Rates 2019')
plt.savefig("Output/Crime_Education_scatter.png")
plt.show()


# In[17]:


# correlation | for every change of the y then the x would change in 2 times (2x) | y = 2x | y = -0.65x 
# the higher the number, the closer the relationship | must be -1 < correlation < 1 (from 0.5 is good relationship)
Graduation = masterdf.iloc[:,5]
Crime = masterdf.iloc[:,2]
correlation = st.pearsonr(Graduation,Crime)
print(f"The correlation between both factors is {round(correlation[0],2)}")


# In[18]:


# Add the linear regression equation and line to plot | y = -0.45x 
x_values = masterdf["graduate ratio (%)"]
y_values = masterdf["Crime Rate"]
(slope, intercept, rvalue, pvalue, stderr) = linregress(x_values, y_values)
regress_values = x_values * slope + intercept
line_eq = "y = " + str(round(slope,2)) + "x + " + str(round(intercept,2))
plt.scatter(x_values,y_values)
plt.plot(x_values,regress_values,"r-")
plt.annotate(line_eq,(6,10),fontsize=15,color="red")
plt.xlabel("Graduation Ratios")
plt.ylabel("Crime Rates")
plt.savefig("Output/Regression_Crime_Education.png")
plt.show()


# In[19]:


x_values = masterdf["graduate ratio (%)"]
y_values = masterdf["Crime Rate"]
(slope, intercept, rvalue, pvalue, stderr) = linregress(x_values, y_values)
regress_values = x_values * slope + intercept
line_eq = "y = " + str(round(slope,2)) + "x + " + str(round(intercept,2))
print(line_eq)


# In[20]:


# Analysis: pls refer to presentation slides and readme file. 


# In[ ]:




