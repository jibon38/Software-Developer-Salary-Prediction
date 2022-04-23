# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 11:16:15 2022
@author: Jibon
"""
import streamlit as st
import pickle
import numpy as np

def load_module():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_module()

regressor = data['model']
le_country = data['le_country']
le_education = data['le_education']

def show_predict_page():
    st.title('Software Developer Salary Prediction')
    st.write('Provide the following information to predict salary')
    #st.write("""### we need some info to predict salary""")      # '##' means <h2> tag

    countries = {'United States of America',
                 'India',
                 'Germany',
                 'United Kingdom of Great Britain and Northern Ireland',
                 'Canada',
                 'France',
                 'Brazil',
                 'Spain',
                 'Netherlands',
                 'Australia',
                 'Poland',
                 'Italy',
                 'Russian Federation',
                 'Sweden',
                 'Turkey',
                 'Switzerland',
                 'Israel',
                 'Norway'}
    education = {"Master’s degree",
                 "Bachelor’s degree",
                 "Postgrad degree",
                 'Less than a Bachelor degree'}
    
    country = st.selectbox("Country", countries)
    education = st.selectbox("Education Level", education)
    experience = st.slider("Years of Experience", 0, 50, 2)
    
    buttonOk = st.button("Calculate Salary")
    
    if buttonOk:
        X = np.array([[country, education, experience]])
        X[:,0] = le_country.transform(X[:,0])
        X[:,1] = le_education.transform(X[:, 1])
        X = X.astype(float)
        
        salary = regressor.predict(X)
        st.subheader(f"Estimated Salary: ${salary[0] : .2f}")













