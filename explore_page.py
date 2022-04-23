# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 11:16:37 2022
@author: Jibon
"""

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def shorteningCountries(countries, cutoff):
    catagorical_map = {}
    for i in range(len(countries)):
        if(countries.values[i] >= cutoff):
            catagorical_map[countries.index[i]] = countries.index[i] 
        else:
            catagorical_map[countries.index[i]] = 'Other_Countries'
    return catagorical_map

def cleanExperience(x):
    if x == 'Less than 1 year':
        return 0.5
    if x == 'More than 50 years':
        return 50
    return float(x)

def cleanEducation(degree):
    if "Master’s degree" in degree:
        return "Master’s degree"
    if "Bachelor’s degree" in degree:
        return "Bachelor’s degree"
    if "Professional degree" in degree or "Other doctoral" in degree:
        return "Postgrad degree"
    return "Less than a Bachelor degree"

@st.cache
def load_data():
    dataset = pd.read_csv('stackoverflow.csv')
    
    dataset = dataset[['Country', 'EdLevel', 'Employment', 'YearsCode', 'ConvertedCompYearly']]
    
    dataset = dataset.rename({'ConvertedCompYearly' : 'Salary'}, axis=1)
    dataset = dataset[dataset['Salary'].notnull()]
    dataset = dataset.dropna()
    
    dataset = dataset[dataset['Employment'] == 'Employed full-time']
    dataset = dataset.drop('Employment', axis=1)
    
    catagorical_map = shorteningCountries(dataset.Country.value_counts(), 400)
    dataset['Country'] = dataset['Country'].map(catagorical_map)
    
    dataset = dataset[dataset['Salary'] <= 250000]
    dataset = dataset[dataset['Salary'] >= 20000]
    dataset = dataset[dataset['Country'] != 'Other_Countries']
    
    dataset['YearsCode'] = dataset['YearsCode'].apply(cleanExperience)
    
    dataset['EdLevel'] = dataset['EdLevel'].apply(cleanEducation)
    
    return dataset

dataset = load_data()


def show_explore_page():
    st.title("Explore Developer's Salary")
    st.write("""### Stack Overflow Developer Survey 2021 """)
    
    data = dataset['Country'].value_counts()
    
    fig, ax = plt.subplots()
    ax.pie(data, labels=data.index, autopct="%1.1f%%", shadow=True, startangle=90)
    ax.axis('equal')
    
    st.write("""#### No of Data from different countries """)
    st.pyplot(fig) 
    
    
    st.write("""
             #### Mean salary based on Country 
             """)
    data = dataset.groupby(['Country'])['Salary'].mean().sort_values(ascending=True)
    st.bar_chart(data)
    
    
    st.write("""
             #### Mean salary based on Experience 
             """)
    data = dataset.groupby(['YearsCode'])['Salary'].mean().sort_values(ascending=True)
    st.line_chart(data)
