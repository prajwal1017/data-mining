from json import load
from xmlrpc.client import Boolean
import streamlit as st
import pandas as pd
import numpy as np
import time 
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
from sklearn import datasets
from sklearn.tree import DecisionTreeClassifier 
from sklearn import tree
from sklearn.tree import _tree


def app(data):
    st.title("Assignment 4")

    # Prepare the data data
    iris = datasets.load_iris()
    X = iris.data
    y = iris.target

    # Fit the classifier with max_depth=3
    clf = DecisionTreeClassifier(max_depth=3, random_state=1234)
    model = clf.fit(X, y)
    st.write(clf)
    
    # get the text representation
    # text_representation = tree.export_text(clf)
    # st.write(text_representation)
    
    # text_representation = tree.export_text(clf, feature_names=iris.feature_names)
    # st.write(text_representation)
    def get_rules(tree, feature_names, class_names):
        tree_ = tree.tree_
        
        feature_name = [
            feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
            for i in tree_.feature
        ]

        path = []
        paths = []

        def recurse(node, path, paths):

            if tree_.feature[node] != _tree.TREE_UNDEFINED:
                name = feature_name[node]
                threshold = tree_.threshold[node]
                p1, p2 = list(path), list(path)
                p1 += [f"({name} <= {np.round(threshold, 3)})"]
                recurse(tree_.children_left[node], p1, paths)
                p2 += [f"({name} > {np.round(threshold, 3)})"]
                recurse(tree_.children_right[node], p2, paths)
            else:
                path += [(tree_.value[node], tree_.n_node_samples[node])]
                paths += [path]

        recurse(0, path, paths)

        # sort by samples count
        samples_count = [p[-1][1] for p in paths]
        ii = list(np.argsort(samples_count))
        paths = [paths[i] for i in reversed(ii)]

        rules = []
        for path in paths:
            rule = "if "

            for p in path[:-1]:
                if rule != "if ":
                    rule += " and "
                rule += str(p)
            rule += " then "
            if class_names is None:
                rule += "response: "+str(np.round(path[-1][0][0][0],3))
            else:
                classes = path[-1][0][0]
                l = np.argmax(classes)
                rule += f"class: {class_names[l]} (proba: {np.round(100.0*classes[l]/np.sum(classes),2)}%)"
            rule += f" | based on {path[-1][1]:,} samples"
            rules += [rule]

        return rules

    rules = get_rules(clf, iris.feature_names, iris.target_names)
    for r in rules:
        st.write(r)
    
    
    