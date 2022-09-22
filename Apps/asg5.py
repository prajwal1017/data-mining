from json import load
from turtle import color
from xmlrpc.client import Boolean
import streamlit as st
import pandas as pd
import numpy as np
import time 
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import plot_confusion_matrix, plot_roc_curve
from sklearn.metrics import precision_score, recall_score, confusion_matrix
from sklearn import metrics
from sklearn.naive_bayes import GaussianNB  
from matplotlib.colors import ListedColormap  
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from statistics import mode
import math
import random
import warnings
def app(data):
    st.title("Assignment 5")
    warnings.filterwarnings('always')  # "error", "ignore", "always", "default", "module" or "once"

    st.set_option('deprecation.showPyplotGlobalUse', False)

    def printf(url):
         st.markdown(f'<p style="color:#000;font:lucida;font-size:25px;">{url}</p>', unsafe_allow_html=True)

    operation = st.selectbox("Operation", ["Regression classifier",'Naive Bayesian Classifier','k-NN classifier', 'ANN'])

    cols = []
    for i in data.columns[:-1]:
        cols.append(i)
    
    classDic = {0:"setosa", 1:"versicolor", 2:"virginica"}
    
    if operation == "Regression classifier":
        #Prepare the training set

        # atr1, atr2 = st.columns(2)
        # attribute1 = atr1.selectbox("Select Attribute 1", cols)
        classatr = data.columns[-1]
       
        

        # X = feature values, all the columns except the last column
        X = data.iloc[:, :-1]

        # y = target values, last column of the data frame
        y = data.iloc[:, -1]

        # plt.xlabel("Feature")
        plt.ylabel(classatr)

        colarr = ['blue','green','red','black']
        i=0
        for attribute in cols:
            pltX = data.loc[:, attribute]
            pltY = data.loc[:,classatr]
            plt.scatter(pltX, pltY, color=colarr[i], label=attribute)
            i += 1

        
        plt.legend(loc=4, prop={'size':8})
        plt.show()
        st.pyplot()

        #Split the data into 80% training and 20% testing
        x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        #Train the model
        model = LogisticRegression()
        model.fit(x_train, y_train) #Training the model
        
        st.subheader("Confusion Matrix")
        plot_confusion_matrix(model, x_test, y_test)
        st.pyplot()
        
        st.subheader("Logistic Regression Results")
        accuracy = model.score(x_test, y_test)
        y_pred = model.predict(x_test)

        st.write("Recognition Rate: ", accuracy.round(2)*100, '%')
        st.write("Misclassification Rate: ", (100.00 - accuracy.round(2)*100), '%')
        st.write("Precision: ", precision_score(y_test, y_pred, average='macro'))
        st.write("Recall(Sensitivity): ", recall_score(y_test, y_pred, average="macro"))
        st.write("Specificity: ", recall_score(y_test, y_pred, pos_label=0, average="macro"))

    if operation == "Naive Bayesian Classifier":
        st.subheader("Naive Baysian classifier")
        classatr = data.columns[-1]
        

        # X = feature values, all the columns except the last column
        X = data.iloc[:, :-1]

        # y = target values, last column of the data frame
        y = data.iloc[:, -1]

        #Split the data into 80% training and 20% testing
        x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        #Train the model
        model = GaussianNB()
        model.fit(x_train, y_train) #Training the model
        
        y_pred = model.predict(x_test) 

        st.subheader("Confusion Matrix")
        plot_confusion_matrix(model, x_test, y_test)
        st.pyplot()
        st.subheader("Results")
        accuracy = model.score(x_test, y_test)
        y_pred = model.predict(x_test)
        st.write("Recognition Rate: ", accuracy.round(2)*100, '%')
        st.write("Misclassification Rate: ", (100.00 - accuracy.round(2)*100), '%')
        st.write("Precision: ", precision_score(y_test, y_pred, average='macro'))
        st.write("Recall(Sensitivity): ", recall_score(y_test, y_pred, average="macro"))
        st.write("Specificity: ", recall_score(y_test, y_pred, pos_label=0, average="macro"))        

          
         
        

        
    if operation == "k-NN classifier":
        # st.dataframe(data)
        atr1, atr2 = st.columns(2)
        kvalue = atr1.select_slider("Enter K value", [1,3,5,7])
        # attribute1 = atr1.number_input("Enter 1st K", value=7)
        # attribute2 = atr2.number_input("Enter 2nd cordinate", value=3)
        
        
        def DetectClass(points,p,k=3):
            
            distance=[]
            for clsAtr in points:
                for feature in points[clsAtr]:
        
                    #calculate the euclidean distance of p from training points 
                    euclidean_distance = math.sqrt((feature[0]-p[0])**2 +(feature[1]-p[1])**2)
        
                    # Add a tuple of form (distance,clsAtr) in the distance list
                    distance.append((euclidean_distance,clsAtr))
        
            # sort the distance list in ascending order
            # and select first k distances
            distance = sorted(distance)[:k]
            st.write("Distance")
            st.dataframe(distance)
            freq1 = 0 #frequency of clsAtr 0
            freq2 = 0 #frequency og clsAtr 1
            freq3 = 0 #frequency for clsAtr 3
            for d in distance:
                # st.write(d[1])
                if d[1] == 0:
                    freq1 += 1
                elif d[1] == 1:
                    freq2 += 1
                elif d[1] == 2:
                    freq3 += 1

            # st.write(freq1)
            # st.write(freq2)
            # st.write(freq3)
        
            if freq2 > freq1 and freq2 > freq3:
                return 1
            
            if freq3 > freq1 and freq3 > freq2:
                return 2
            
            return 0
        
        # driver function
        def main():
            p = (attribute1, attribute2)

            cols = []
            for i in data.columns[:-1]:
                cols.append(i)

            
            atr1, atr2 ,atr3, atr4 = cols

            arrp=[]
            for j in range(50):
                arrp.append((data.loc[j, atr1], data.loc[j, atr2]))
                arrp.append((data.loc[j, atr3], data.loc[j, atr4]))
                j += 3
            st.write("Sample points")
            st.write(arrp)
            arr1List = []
            for j in range(50):
                arr1List.append((data.loc[j, atr1], data.loc[j, atr2]))
                arr1List.append((data.loc[j, atr3], data.loc[j, atr4]))
                
                if j>=50:
                    break
            res1 = arr1List.copy()
            arr1List.clear()
            # st.write("RES 1")
            # st.write(res1)
            for j in range(50, 100):
                arr1List.append((data.loc[j, atr1], data.loc[j, atr2]))
                arr1List.append((data.loc[j, atr3], data.loc[j, atr4]))
                
                if j>=100:
                    break
            
            res2 = arr1List.copy()
            arr1List.clear()
            # st.write("RES 2")
            # st.write(res2)
            for j in range(100, 150):
                arr1List.append((data.loc[j, atr1], data.loc[j, atr2]))
                arr1List.append((data.loc[j, atr3], data.loc[j, atr4]))
                
                if j>=150:
                    break
            
            res3 = arr1List.copy()
            arr1List.clear()
            # st.write("RES 3")
            # st.write(res3)
            #st.write(arr1List)
        
            points = {
                0:res1,
                1:res2,
                2:res3
            }

            # st.table(points)
            # Number of neighbours 
            
            k = st.number_input("Enter value of k", min_value=1, max_value=7, step=2)
            
            ans = DetectClass(points,p,k)
            st.write(f"The value classified to unknown point is: {classDic[ans]}")
            
        
       
        randomlist = []
        for i in range(150):
            randomlist.append(random.randint(0,7))
        # print(randomlist)
        # st.header("Manually")
        # main()
        
        def inbuilt():
            df = data
            classatr = data.columns[-1]
            scaler = StandardScaler()
            
            scaler.fit(df.drop(classatr, axis = 1))
            scaled_features = scaler.transform(df.drop(classatr, axis = 1))
            
            df_feat = pd.DataFrame(scaled_features, columns = df.columns[:-1])
            df_feat.head()
            
            X_train, X_test, y_train, y_test = train_test_split(
                scaled_features, df[classatr], test_size = 0.30)

            # Remember that we are trying to come up
            # with a model to predict whether
            # someone will TARGET CLASS or not.
            # We'll start with k = 1.

            
            knn = KNeighborsClassifier(n_neighbors = kvalue)

            knn.fit(X_train, y_train)
            y_pred = knn.predict(X_test)

            # st.write("X_test")
            # st.write(X_test)

            # st.write("Y_test")
            # st.write(y_test)

            # st.write("X_train")
            # st.write(X_train)

            # st.write("Y_train")
            # st.write(y_train)

            # st.write("y_pred")
            # st.write(y_pred)


            classMap = {
                'Setosa':0,
                'Versicolor':1,
                'Virginica':2
            }


           
           

            accuracy = knn.score(X_test, y_test)
      

            st.subheader("Confusion Matrix")
            plot_confusion_matrix(knn, X_test, y_test)
            st.pyplot()
            
            st.write("Recognition Rate: ", accuracy.round(2)*100, '%')
            st.write("Misclassification Rate: ", (100.00 - accuracy.round(2)*100), '%')
            st.write("Precision: ", precision_score(y_test, y_pred, average='macro'))
            st.write("Recall(Sensitivity): ", recall_score(y_test, y_pred, average="macro"))
            st.write("Specificity: ", recall_score(y_test, y_pred, pos_label=0, average="macro"))


            # Predictions and Evaluations
            # Let's evaluate our KNN model !
            # from sklearn.metrics import classification_report, confusion_matrix
            # st.write(confusion_matrix(y_test, pred))

            # st.write(classification_report(y_test, pred))

        # st.header("In Built")
        inbuilt()