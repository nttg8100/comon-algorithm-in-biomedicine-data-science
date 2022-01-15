# Load library
from sklearn import datasets
from sklearn.pipeline import make_pipeline
import numpy as np
import pandas as pd
import scipy.stats as sps
from sklearn import linear_model
from sklearn.metrics import roc_curve, RocCurveDisplay, auc
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

import sys

# Data directory
file = sys.argv[1]

df = pd.read_csv(file)

features = df.columns.drop("target").tolist()

models = pd.DataFrame(
    columns=['x', 'y', 'proba', 'tpr', 'fpr', 'youden_j', 'model_name'])

for i in features:
    print("Calculating using single variable with the features:", i)
    X_train, X_test, y_train, y_test = train_test_split(
        df.drop(columns="target"), df.target.values, test_size=0.3, random_state=1)
    # split dataset into train-test
    # init and fit Logistic Regression on train set
    clf = linear_model.LogisticRegression(max_iter=3000)
    clf.fit(X_train, y_train)
    # predict probabilities on x test set
    y_proba = clf.predict_proba(X_test)
    # compute FPR and TPR from y test set and predicted probabilities
    fpr, tpr, thresholds = roc_curve(
        y_test, y_proba[:, 1], drop_intermediate=False)
    # compute ROC AUC
    roc_auc = auc(fpr, tpr)
    # init a dataframe for results
    df_test = pd.DataFrame({
        "x": X_test[[i]].values.flatten(),
        "y": y_test,
        "proba": y_proba[:, 1]
    })
    # sort it by predicted probabilities
    # because thresholds[1:] = y_proba[::-1]
    df_test.sort_values(by="proba", inplace=True)
    # add reversed TPR and FPR
    df_test["tpr"] = tpr[1:][::-1]
    df_test["fpr"] = fpr[1:][::-1]
    # optional: add thresholds to check
    #df_test["thresholds"] = thresholds[1:][::-1]
    # add Youden's j index
    df_test["youden_j"] = df_test.tpr - df_test.fpr
    df_test["model_name"] = i
    # define the cut_off and diplay it
    cut_off = df_test.sort_values(
        by="youden_j", ascending=False, ignore_index=True).iloc[0]
    print("CUT-OFF:")
    print(cut_off)
    models = models.append(cut_off.to_dict(), ignore_index=True)

models.to_csv("models_youden_j.csv", index=False)
