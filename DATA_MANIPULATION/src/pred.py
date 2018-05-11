# coding: utf-8
# Regression Linéaire Multiple

# Importer les librairies
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv


def setdata(X, is_train_set):
    X = X.tolist()
    indice = 12 if is_train_set else 11
    X = [[i for i in line if line.index(i) != indice] for line in X]
    indice = 7 if is_train_set else 6
    X = [[i for i in line if line.index(i) != indice] for line in X]
    if  is_train_set:
        X = [[i for i in line if line.index(i) != 4] for line in X]
    X = [[i for i in line if line.index(i) != 1] for line in X]
    X = [line[1:] for line in X]
    X = [[str(col).replace('-', '') for col in line] for line in X]
    X = [[str(col).replace('ouvre', '0') for col in line] for line in X]
    X = [[str(col).replace('WE', '1') for col in line] for line in X]
    newX=[]
    for line in X :
        heure = line[1].split(':')
        date = line[0].split('-')
        line = [i for i in line if line.index(i) > 1]
        line.extend(heure)
        line.extend(date)
        newX.append(line)
    return np.array(newX).astype(float)



# Importer le dataset
dataset = pd.read_csv('trainset.csv')
X_train = dataset.iloc[:, :].values 
y_train = dataset.iloc[:, 4].values
X_train = setdata(X_train, True)

dataset = pd.read_csv('testset_2017-07-12.csv')
X_test = dataset.iloc[:, :].values 
y_test = dataset.iloc[:, 4].values
X_test = setdata(X_test, False)

dataset = pd.read_csv('testset_2017-07-13.csv')
X_test1 = dataset.iloc[:, :].values 
y_test1 = dataset.iloc[:, 4].values
X_test1 = setdata(X_test1, False)

# Construction du modèle
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(X_train, y_train)
# Predictions
y_pred = regressor.predict(X_test)
y_pred1 = regressor.predict(X_test1)

#  Creation du fichier csv
resultats = open('resultats_2017-07-12.csv', "w+")
resultats1 = open('resultats_2017-07-13.csv', "w+")
fieldnames = ["region.code", "date", "hour","pred"]
resultats = csv.DictWriter(resultats, fieldnames=fieldnames)
resultats.writeheader()
resultats1 = csv.DictWriter(resultats1, fieldnames=fieldnames)
resultats1.writeheader()

# Write data
j=0
for line in X_test:
    hours = line[6]
    if hours >= 1:
        hours = int(hours)
    else:
        hours = str(hours).replace('.', '')
    hours = str(hours)
    minutes = line[7]
    if minutes >= 1:
        minutes = int(minutes)
    else:
        minutes = str(minutes).replace('.', '')
    minutes = str(minutes)
    y_pred[j] = int(y_pred[j])
    pred = str(y_pred[j])
    pred = pred.replace('.0', '')
    pred = int(pred)
    row = {'region.code': 'FRANCE', 'date': '2017-07-12', 'hour': hours + ':' + minutes, 'pred': pred}
    resultats.writerow(row)
    j+=1

j=0
for line in X_test1:
    hours = line[6]
    if hours >= 1:
        hours = int(hours)
    else:
        hours = str(hours).replace('.', '')
    hours = str(hours)
    minutes = line[7]
    if minutes >= 1:
        minutes = int(minutes)
    else:
        minutes = str(minutes).replace('.', '')
    minutes = str(minutes)
    y_pred1[j] = int(y_pred1[j])
    pred = str(y_pred1[j])
    pred = pred.replace('.0', '')
    pred = int(pred)
    row = {'region.code': 'FRANCE', 'date': '2017-07-12', 'hour': hours + ':' + minutes, 'pred': pred}
    resultats1.writerow(row)
    j+=1




