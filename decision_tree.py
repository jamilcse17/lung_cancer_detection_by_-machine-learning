import numpy as np
import pandas as pd
from pandas import read_csv
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_val_score
from os import system
from sklearn.impute import SimpleImputer

accuracy=[]
cv=[]
fsc=[]
for i in range(0,10):
    data = read_csv("lung_cancer.csv")
    X=data.iloc[:,1:].values
    Y=data.iloc[:,0]

    imp = SimpleImputer(missing_values='?', strategy='most_frequent')
    X=imp.fit_transform(X)
    X=pd.DataFrame(X)

    X_train, X_test, Y_train, Y_test =train_test_split(X,Y, test_size=0.2)

    decisionTreeClassifier = tree.DecisionTreeClassifier(criterion="entropy")
    dTree = decisionTreeClassifier.fit(X, Y)
    cross_val= np.max(cross_val_score(dTree,X_train,Y_train,cv=5))
    Y_pred=dTree.predict(X_test)
    cm= confusion_matrix(Y_test, Y_pred)
    print("\nCross Validation Score: ", cross_val)
    cv.append(cross_val)
    print("\nConfusion Matrix: ")
    print(cm)
    acc=(metrics.accuracy_score(Y_test,Y_pred))
    acc=acc*100
    print("\nAccuracy Score: ", "{:.2f}".format(acc),"%")
    fs=metrics.f1_score(Y_test,Y_pred,average='micro')
    print("\nF1 Score: ",fs)
    fsc.append(fs)
    accuracy.append(acc)


print("\nRecorded accuracy for Ten Times: ",accuracy)
print("\nRecorded F1 Score for Ten Times: ",fsc)
print("\nRecorded Cross Validation Score for Ten Times: ",cv)
print("\nMaximum Cross Validation Score recorded: ", max(cv))
print("\nMaximum F1 Score recorded: ", max(fsc))
print("\nMaximum accuracy recorded: ", max(accuracy),"%")
dotfile = open("dtree.dot", 'w')
tree.export_graphviz(dTree, out_file = dotfile, feature_names = X.columns)
dotfile.close()
