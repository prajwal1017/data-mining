from calendar import c
from json import load
import math
from xmlrpc.client import Boolean
import streamlit as st
import pandas as pd
import numpy as np
import scipy.stats as stats
import math
import time 
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
import seaborn as sns


import io
import requests

def app(data):
    
    # convert the dictionary into DataFrame
    df = pd.DataFrame(data)
    # df.drop(['Id'], axis=1)
    classatr = df.columns[-1]
    
    def compute_impurity(feature, impurity_criterion):
        
        probs = feature.value_counts(normalize=True)
        
        if impurity_criterion == 'entropy':
            impurity = -1 * np.sum(np.log2(probs) * probs)
        elif impurity_criterion == 'gini':
            impurity = 1 - np.sum(np.square(probs))
        else:
            raise ValueError('Unknown impurity criterion')
            
        return(round(impurity, 3))
    
    target_entropy = compute_impurity(df[classatr], 'entropy')
    target_entropy
    
    df[classatr].value_counts()
    
    for level in df[classatr].unique():
        st.write('level name:', level)
        df_feature_level = df[df[classatr] == level]
        st.write('corresponding data partition:')
        st.write(df_feature_level)
        st.write('partition target feature impurity:', compute_impurity(df_feature_level[classatr], 'entropy'))
        st.write('partition weight:', str(len(df_feature_level)) + '/' + str(len(df)))
        st.write('====================')
    
    def comp_feature_information_gain(df, target, descriptive_feature, split_criterion):
        """
        This function calculates information gain for splitting on 
        a particular descriptive feature for a given dataset
        and a given impurity criteria.
        Supported split criterion: 'entropy', 'gini'
        """
        
        st.write('target feature:', target)
        st.write('descriptive_feature:', descriptive_feature)
        st.write('split criterion:', split_criterion)
                
        target_entropy = compute_impurity(df[target], split_criterion)
    
        # we define two lists below:
        # entropy_list to store the entropy of each partition
        # weight_list to store the relative number of observations in each partition
        entropy_list = list()
        weight_list = list()
        
        # loop over each level of the descriptive feature
        # to partition the dataset with respect to that level
        # and compute the entropy and the weight of the level's partition
        for level in df[descriptive_feature].unique():
            df_feature_level = df[df[descriptive_feature] == level]
            entropy_level = compute_impurity(df_feature_level[target], split_criterion)
            entropy_list.append(round(entropy_level, 3))
            weight_level = len(df_feature_level) / len(df)
            weight_list.append(round(weight_level, 3))
    
        # st.write('impurity of partitions:', entropy_list)
        # st.write('weights of partitions:', weight_list)
    
        feature_remaining_impurity = np.sum(np.array(entropy_list) * np.array(weight_list))
        st.write('remaining impurity:', feature_remaining_impurity)
        
        information_gain = target_entropy - feature_remaining_impurity
        st.write('information gain:', information_gain)
        
        st.write('====================')
    
        return(information_gain)
    
    split_criterion = 'entropy'
    for feature in df.drop(columns=classatr).columns:                
        feature_info_gain = comp_feature_information_gain(df, classatr, feature, split_criterion)
        st.write(feature_info_gain)
    
    split_criteria = 'gini'
    for feature in df.drop(columns=classatr).columns:
        feature_info_gain = comp_feature_information_gain(df, classatr, feature, split_criteria)
        st.write(feature_info_gain)
    

