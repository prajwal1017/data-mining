from json import load
import streamlit as st
import pandas as pd
import numpy as np
import time 
import matplotlib.pyplot as plt
from multiapp import MultiApp
from Apps import asg1, asg2, asg3, asg4, asg5


#variables
disrad = False

st.title("Data Analysis Tool")
file = st.file_uploader("Enter Dataset first to Proceed", type=['csv'], accept_multiple_files=False,disabled=False)

# data = pd.read_csv(file)

def load_file():
    df = pd.read_csv(file)
    st.header("Dataset Table")
    st.dataframe(df, width=1000, height=500)
    return df
if file:
    data = load_file()  
    
    app = MultiApp()
    
    app.add_app("Assignment 1. Central tendency, Dispersion, Plots", asg1.app)
    app.add_app("Assignment 2. Correlation and Normalization", asg2.app)
    app.add_app("Assignment 3. Entropy, Info Gain, Gini", asg3.app)
    app.add_app("Assignment 4. Rules based classifier", asg4.app)
    app.add_app("Assignment 5. Naive Bays, KNN, ANN", asg5.app)
    # The main app
    app.run(data)

