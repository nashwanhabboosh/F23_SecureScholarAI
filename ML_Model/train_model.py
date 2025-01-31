import pandas as pd
from preprocessing import preprocess
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pickle
from flask import Flask
from flask import request
import numpy as np
import random
##idk why i never pushed this to the repo...

data = pd.read_csv("./Dataset/train_snli.csv",sep = "\t",header=0,names = ['Phrase','Suspicious','Class'])
#data provided by https://www.kaggle.com/code/mpwolke/plagiarism-mit-detection
data = data.dropna()[:4000]

X,y,vocab = preprocess(data)

X = [[X[0][x],X[0][d],y[x]] if d==x else [X[0][x],X[0][d],0] for d in range(len(X[1])) for x in range(len(X[0]))]
y = [X[x][-1] for x in range(len(X))]
X = [[np.array(X[x][:-1]).astype(np.float32) for x in range(len(X))]]

X=np.array(X)[0]
X = X.reshape(len(X),-1)

y_1 = np.array(y)[np.array(y)==1]
X_1 = X[np.array(y)==1]
y_0 = random.sample(list(enumerate(np.array(y)[np.array(y)==0])),sum(np.array(y)==1))
X_0 = X[np.array(y_0)[:,0]]

y_ = np.concatenate((y_1,np.array(y_0)[:,1]))
X_ = np.concatenate((X_1,X_0))

shuf = list(range(len(y_)))

random.shuffle(shuf)
X = X_[shuf]
y = y_[shuf]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

logreg_model = LogisticRegression()
logreg_model.fit(X_train, y_train)
y_pred = logreg_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
classification_rep = classification_report(y_test, y_pred)

print("Accuracy:", accuracy)
print("Classification Report:")
print(classification_rep) #save trained model
pickle.dump(logreg_model, open("./trained_models/logistic_regression.sav", 'wb'))

tree_model = DecisionTreeClassifier() #reached an accuracy of 98.62%
tree_model.fit(X_train, y_train)
y_pred = tree_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
classification_rep = classification_report(y_test, y_pred)

print("Accuracy:", accuracy)
print("Classification Report:")
print(classification_rep)

pickle.dump(tree_model, open("./trained_models/decision_tree.sav", 'wb'))


#analysis

#find most important features (word chunks) for detecting plagiarism:
l=np.argsort(tree_model.feature_importances_)[-10:]
important_phrase = np.array(list(vocab.keys()))[l]