#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies
import numpy as np
import json
import pandas as pd
import matplotlib.pyplot as plt
import requests
from pprint import pprint
from config import crimekey
from config import censuskey
from census import Census
c = Census(censuskey, year=2013)


# In[2]:


# Read CSVs
edupath = "Resources/cc_institution_details_clean.csv"
#crimepath = 

edu = pd.read_csv(edupath,encoding='utf-8')
#crime = pd.read_csv(crimepath)

edu.head()


# In[3]:


edu.columns


# In[4]:


edu_df = edu[["state","level","basic","level","student_count"]]
edu_df.head()


# In[5]:


# API set up for nation-wide 2019

baseurl = "http://api.usa.gov/crime/fbi/sapi/"

#URL = ("https://api.usa.gov/crime/fbi/sapi/api/summarized/state/AL/violent-crime/2019/2019?API_KEY=" + crimekey)

stateAbbs = ['AL', 'AK', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS',
            'KY', 'LA', 'MA', 'ME', 'MD', 'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 
            'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']
statedict = {}
record = 1

# loop through all states and pull data for each
for item in stateAbbs:
    query_url = "https://api.usa.gov/crime/fbi/sapi/api/summarized/state/" + item + "/violent-crime/2019/2019?API_KEY=" + crimekey
    # Get response into JSON
    stateresponse = requests.get(query_url)
    statejson = stateresponse.json()
    x = len(statejson['results'])
    # Log each state and account for exceptions
    try:
        # Collect crime data and put it into a dictionary
        actuals = 0
        for i in range(x):
            actuals = actuals + statejson['results'][i]['actual']
            statedict[item] = [actuals]
        print(f"Processing record {record} | {item}")
        record += 1
        
            
    # Exception if state data isn't found
    except:
        print(f"Data not found for {item}. Skipping...")

print("----------Job complete!----------")


# In[69]:


# convert crime data into dataframe
# Convert the dictionary into a dataframe
statedf = pd.DataFrame.from_dict(statedict, orient='index')
statedf.head()
statedf.to_csv("Output/statedf.csv", index=False, header=True)


# In[7]:


# API set up for crime nation-wide 2019

baseurl = "http://api.usa.gov/crime/fbi/sapi/"
#URL = ("https://api.usa.gov/crime/fbi/sapi/api/summarized/state/AL/violent-crime/2019/2019?API_KEY=" + crimekey)

#getdatasets = requests.get(URL)
#datasets_json = getdatasets.json()
#pprint(datasets_json)

stateAbbs = ['AL', 'AK', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS',
            'KY', 'LA', 'MA', 'ME', 'MD', 'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 
            'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']
statedict = {}
record = 1

# loop through all states and pull data for each
for item in stateAbbs:
    query_url = "https://api.usa.gov/crime/fbi/sapi/api/summarized/state/" + item + "/violent-crime/2019/2019?API_KEY=" + crimekey
   
    # Get response into JSON
    stateresponse = requests.get(query_url)
    statejson = stateresponse.json()
    pprint(statejson)


# In[ ]:


# calculate the total actual cases per state: #extract ~+-20 rows of each state to sum up
# create df of crime per state
#AL = ["AL"]

# set up lists to hold reponse info
#actualAL = []

# Loop through the list of cities and perform a request for data on each
#for item in stateAbbs:
    #responseAL = requests.get("https://api.usa.gov/crime/fbi/sapi/api/summarized/state/AL/violent-crime/2019/2019"+
     #                         "?API_KEY="+ crimekey).json()
    #pprint(response)
    #actualAL.append(responseAL["results"]["actual"])
    #print(actualAL)

#AL_crime = sum(actualAL)
#print(AL_crime)


# In[ ]:


# API Setup to get crime data of CA only in 2020
#base_url = "http://api.usa.gov/crime/fbi/sapi/"
#c = Census(censuskey, year=2019)

#URL = ("https://api.usa.gov/crime/fbi/sapi/api/summarized/state/CA/violent-crime/2020/2020?API_KEY=" + crimekey)

#getdatasets = requests.get(URL)
#datasets_json = getdatasets.json()
#pprint(datasets_json)


# In[66]:


# Run Census Search to retrieve data on all states
# Note the addition of "B23025_005E" for unemployment count
census_data = c.acs5.get(("NAME", "B19013_001E", "B01003_001E", "B01002_001E",
                          "B19301_001E",
                          "B17001_002E",
                          "B23025_005E"), {'for': 'state:*'})

# Convert to DataFrame
census_pd = pd.DataFrame(census_data)

# Column Reordering
census_pd = census_pd.rename(columns={"B01003_001E": "Population",
                                      "B01002_001E": "Median Age",
                                      "B19013_001E": "Household Income",
                                      "B19301_001E": "Per Capita Income",
                                      "B17001_002E": "Poverty Count",
                                      "B23025_005E": "Unemployment Count",
                                      "NAME": "Name", "state": "State"})

# Add in Poverty Rate (Poverty Count / Population)
census_pd["Poverty Rate"] = 100 *     census_pd["Poverty Count"].astype(
        int) / census_pd["Population"].astype(int)

# Add in Employment Rate (Employment Count / Population)
census_pd["Unemployment Rate"] = 100 *     census_pd["Unemployment Count"].astype(
        int) / census_pd["Population"].astype(int)

# Final DataFrame
census_pd = census_pd[["State", "Name", "Population", "Median Age", "Household Income",
                       "Per Capita Income", "Poverty Count", "Poverty Rate", "Unemployment Rate"]]

census_pd.head()


# In[68]:


census_pd.to_csv("Output/census_raw.csv")


# In[9]:


# create df of population
population = census_pd[["Name","Population"]]
population = population.rename(columns={"Name": "state"})
population.head()


# In[10]:


# create df education graduation
edu_graduate = edu_df[["state","student_count"]]
edu_graduate.head()


# In[11]:


# merge to have df ab population and graduation then find the gradu rate column
edu_rate_df = pd.merge(edu_graduate,population,how = "left")
edu_rate_df = edu_rate_df.rename(columns={"student_count": "number of graduates"})
edu_rate_df.head()


# In[13]:


#calculate the graduate % and add into new column
edu_rate_df["% graduate"] = edu_rate_df["number of graduates"]/edu_rate_df["Population"]*100
edu_rate_df.head()


# In[81]:


edu_groupby = edu_rate_df.groupby(["state"])
edu_groupby.mean()
edu_groupby.head()


# In[70]:


edu_rate_df.to_csv("Output/edu_rate_df.csv", index=False, header=True)


# In[72]:


# convert the statenames in to one format of AL to do merge to get master dataF

stateNames = {
  "AL" : "Alabama",
  "AK" : "Alaska",
  "AZ" : "Arizona",
  "AR" : "Arkansas",
  "CA" : "California",
  "CO" : "Colorado",
  "CT" : "Connecticut",
  "DE" : "Delaware",
  "FL" : "Florida",
  "GA" : "Georgia",
  "HI" : "Hawaii",
  "ID" : "Idaho",
  "IL" : "Illinois",
  "IN" : "Indiana",
  "IA" : "Iowa",
  "KS" : "Kansas",
  "KY" : "Kentucky",
  "LA" : "Louisiana",
  "ME" : "Maine",
  "MD" : "Maryland",
  "MA" : "Massachusetts",
  "MI" : "Michigan",
  "MN" : "Minnesota",
  "MS" : "Mississippi",
  "MO" : "Missouri",
  "MT" : "Montana",
  "NE" : "Nebraska",
  "NV" : "Nevada",
  "NH" : "New Hampshire",
  "NJ" : "New Jersey",
  "NM" : "New Mexico",
  "NY" : "New York",
  "NC" : "North Carolina",
  "ND" : "North Dakota",
  "OH" : "Ohio",
  "OK" : "Oklahoma",
  "OR" : "Oregon",
  "PA" : "Pennsylvania",
  "RI" : "Rhode Island",
  "SC" : "South Carolina",
  "SD" : "South Dakota",
  "TN" : "Tennessee",
  "TX" : "Texas",
  "UT" : "Utah",
  "VT" : "Vermont",
  "VA" : "Virginia",
  "WA" : "Washington",
  "WV" : "West Virginia",
  "WI" : "Wisconsin",
  "WY" : "Wyoming",
  "DC" : "District of Columbia"
}

stateNamedf = pd.DataFrame.from_dict(stateNames, orient='index')
stateNamedf.reset_index()
#stateNamedf


# In[50]:


# Merge the datasets to have the state columns in shortage AL format

#statedf = pd.merge(statedf, stateNamedf, how = "outer")
#edu_crime.rename(columns={'0_x': 'Actuals', '0_y': 'Name'}, inplace=True)

#state_crime = pd.concat([statedf, stateNamedf], axis = 1)
#state_crime.head(10)
#state_crime.reset_index(0)


# In[56]:


# Merge the datasets using the sate columns
statemerge = pd.merge(statedf, stateNamedf, left_index=True, right_index=True)
statemerge.rename(columns={'0_x': 'Actuals', '0_y': 'state'}, inplace=True)
statemerge.reset_index()
statemerge.head()


# In[71]:


statemerge.to_csv("Output/statemerge.csv", index=False, header=True)


# In[1]:


# merge two df together to get master_plot_df : continue in Tracie_shortcut file


# In[ ]:




