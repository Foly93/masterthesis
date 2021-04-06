#!/usr/bin/env python
# coding: utf-8

# In[79]:


import math
import rdkit
import sklearn
import numpy as np
import pandas as pd
from numpy import mean
from numpy import interp
from matplotlib import pyplot
from numpy.random import randint
from sklearn.metrics import roc_curve
from imblearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE
from sklearn.metrics import roc_auc_score
from imblearn.over_sampling import SMOTENC
from sklearn.metrics import confusion_matrix
from sklearn.metrics import matthews_corrcoef
from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import balanced_accuracy_score
from imblearn.under_sampling import RandomUnderSampler
from sklearn.model_selection import RandomizedSearchCV
from sklearn.experimental import enable_halving_search_cv
from sklearn.model_selection import HalvingRandomSearchCV


# In[80]:


def evaluate_model(outer_true,outer_pred,outer_prob):
    
    # print statement and list elements are appended into single arrays for convenience
    print("\nEvaluation of the Validation Set:\n")
    y_true = np.hstack(outer_true)
    y_pred = np.hstack(outer_pred)
    y_prob = np.vstack(outer_prob)[:,-1]
    
    
    # confusion matrix is printed using built in functions
    conf_matrix = confusion_matrix(y_true, y_pred)
    print(conf_matrix)
    
    
    # classification report and other metrics are generated
    print(classification_report(y_true, y_pred))
    print('balanced_acc_score:\t{}\n'.format(balanced_accuracy_score(y_true, y_pred)))
    print('matthews_corr_coef:\t{}\n'.format(matthews_corrcoef(y_true, y_pred)))


    # Sensitivity and specificity are calculated from the confusion matrix and are then printed
    Sensitivity = conf_matrix[0,0]/(conf_matrix[0,0]+conf_matrix[0,1])
    Specificity = conf_matrix[1,1]/(conf_matrix[1,0]+conf_matrix[1,1]) 
    print('Sensitivity:\t{}\n'.format(Sensitivity))
    print('Specificity:\t{}\n'.format(Specificity))

    
    # AUC is calculated from the probabilities and the true y values
    AUC_base_model = roc_auc_score(y_true, y_prob)
    print("AUC-ROC:\t{}\n".format(AUC_base_model))
    
    # calculate and print the ROC from the aggregated (i.e. stacked) outer predictions and plot the graph
    pyplot.figure(1,figsize=(5, 5))    
    FPR, TPR, _ = roc_curve(y_true, y_prob)
    pyplot.xlim([-0.01, 1.01])
    pyplot.ylim([-0.01, 1.01])
    pyplot.plot(FPR, TPR, 'r', label='aggregated ROC')
    pyplot.xlabel('False Positive Rate')
    pyplot.ylabel('True Positive Rate')
    pyplot.legend()
    pyplot.savefig("../_output/fp_651744_agg_auc.svg", dpi=300)
    
    # calculate the averaged ROC by iterating over the individuals outer predictions
    pyplot.figure(0,figsize=(5, 5))
    tprs = []
    base_fpr = np.linspace(0, 1, 101)
    i = 1
    for _true, _prob in zip(outer_true,outer_prob):
        fpr, tpr, _ = roc_curve(_true, _prob[:, 1])
        # alpha means the opacity of the line
        pyplot.plot(fpr, tpr, 'r', alpha=0.15,label='%s-th Outer fold' % i)
        # interp adjusts the number of datapoints to base_fpr (101)
        tpr = interp(base_fpr, fpr, tpr)
        # setting the first element of tpr 0 adjusts for a possible artifact of interp()
        tpr[0] = 0.0
        tprs.append(tpr)
        i = i + 1
    
    # calculate the standard deviation and thereby the upper and lower limits of the averaged ROC
    tprs = np.array(tprs)
    mean_tprs = tprs.mean(axis=0)
    std = tprs.std(axis=0)
    tprs_upper = np.minimum(mean_tprs + std, 1)
    tprs_lower = mean_tprs - std

    # plot the averaged ROC and output the figure to an svg file
    pyplot.plot(base_fpr, mean_tprs, 'r', label='avr. ROC')
    pyplot.fill_between(base_fpr, tprs_lower, tprs_upper, color='grey', alpha=0.3, label='STD+-')
    pyplot.xlim([-0.01, 1.01])
    pyplot.ylim([-0.01, 1.01])
    pyplot.xlabel('False Positive Rate')
    pyplot.ylabel('True Positive Rate')
    pyplot.axes().set_aspect('equal', 'datalim')
    pyplot.title('Averaged AUC-ROC')
    pyplot.legend()
    pyplot.savefig("../_output/fp_651744_avr_auc.svg", dpi=300)
    
    # write the aforementioned metrics into a file
    f = open("../_output/fp_651744_analysis.txt","w+")
    f.write(str(conf_matrix)+'\n')
    f.write(classification_report(y_true, y_pred)+'\n')
    f.write('Balanced Accuracy:\t'+str(balanced_accuracy_score(y_true, y_pred))+'\n')
    f.write('Matthews Coeffici:\t'+str(matthews_corrcoef(y_true, y_pred))+'\n')
    f.write('Sensitivity:\t\t'+str(Sensitivity)+'\n')
    f.write('Specificity:\t\t'+str(Specificity)+'\n')
    f.write('AUC-ROC:\t\t'+str(AUC_base_model)+'\n')
    f.close() 


# In[81]:


def evaluate_training(inner_true,inner_pred,inner_prob):
    
    # print statement and list elements are appended into single arrays for convenience
    print("Evaluation of the Training Set:\n")
    training_true = np.hstack(inner_true)
    training_pred = np.hstack(inner_pred)
    training_prob = np.vstack(inner_prob)


    # confusion matrix is printed using built in functions
    conf_matrix = confusion_matrix(training_true, training_pred)
    print(conf_matrix)


    # calculate and print the ROC from the aggregated (i.e. stacked) inner predictions and plot the graph
    pyplot.figure(1,figsize=(5, 5))
    FPR, TPR, _ = roc_curve(training_true, training_prob[:,1])
    pyplot.plot(FPR, TPR, 'b', label='Base Model')
    pyplot.xlim([-0.01, 1.01])
    pyplot.ylim([-0.01, 1.01])
    pyplot.xlabel('False Positive Rate')
    pyplot.ylabel('True Positive Rate')
    pyplot.title('K-Fold-aggregated AUC-ROC')
    pyplot.legend()

    # calculate the averaged ROC by iterating over the individuals inner predictions
    tprs = []
    base_fpr = np.linspace(0, 1, 101)
    pyplot.figure(0,figsize=(5, 5))
    i = 1
    for _true, _prob in zip(inner_true,inner_prob):
        fpr, tpr, _ = roc_curve(_true, _prob[:, 1])
        pyplot.plot(fpr, tpr, 'b', alpha=0.15, label='%s-th outer Fold' % i)
        tpr = interp(base_fpr, fpr, tpr)
        tpr[0] = 0.0
        tprs.append(tpr)
        i = i + 1

    # calculate the standard deviation and thereby the upper and lower limits of the averaged ROC
    tprs = np.array(tprs)
    mean_tprs = tprs.mean(axis=0)
    std = tprs.std(axis=0)
    tprs_upper = np.minimum(mean_tprs + std, 1)
    tprs_lower = mean_tprs - std

    # plot the averaged ROC and output the figure to an svg file
    pyplot.plot(base_fpr, mean_tprs, 'b', label='avr. ROC')
    pyplot.fill_between(base_fpr, tprs_lower, tprs_upper, color='grey', alpha=0.3, label='STD+-')
    pyplot.xlim([-0.01, 1.01])
    pyplot.ylim([-0.01, 1.01])
    pyplot.xlabel('False Positive Rate')
    pyplot.ylabel('True Positive Rate')
    pyplot.axes().set_aspect('equal', 'datalim')
    pyplot.title('Averaged AUC-ROC')
    pyplot.legend()


# In[82]:


# read the dataframe into RAM
df = pd.read_csv('../../02-CorrectingAssays/_output/cp_651744.csv')

# Assign meta_cols which happen to be the first 10 columns and input cols (the rest of the cols)
meta_cols = df.columns[:10]
input_cols = df.columns[10:]

X = np.array(df.loc[:,input_cols])
df['PUBCHEM_ACTIVITY_OUTCOME'] = df['PUBCHEM_ACTIVITY_OUTCOME'].astype('category').cat.codes
y = df['PUBCHEM_ACTIVITY_OUTCOME'].values

# get the number of samples of actives and inactives of the assay
N_1 = df.PUBCHEM_ACTIVITY_OUTCOME.value_counts().to_list()[0]
N_2 = df.PUBCHEM_ACTIVITY_OUTCOME.value_counts().to_list()[1]

# calculate the relative amount of the minority class to majority class for input in the SMOTE function
sampling_prsnt = round(np.exp(-abs(math.log(N_1/N_2))),2)
sampling_smote = 2 * sampling_prsnt


# In[83]:


# %%time
# define lists to append the model outputs to
outer_pred = []
outer_true = []
outer_prob = []

inner_pred = []
inner_true = []
inner_prob = []

# starter outer validation Loop
skf = StratifiedKFold(n_splits=5)
print("outer split method:\t{}\n".format(skf))
for train_index, test_index in skf.split(X, y):
    
    # define Datasets, Cross-Validation Metrics and Model-Type
    X_innerCV, X_outerCV = X[train_index], X[test_index]
    y_innerCV, y_outerCV = y[train_index], y[test_index]
    cv = ShuffleSplit(n_splits=5,test_size=0.25, random_state=0)
    rf = RandomForestClassifier(n_jobs=-1)
    
    
    # SMOTE-Sampling is used to over sample the minority class and the majority class is undersampled
    if (sampling_prsnt < 0.5) & (sampling_smote < 0.75):
        over = SMOTE(sampling_strategy=sampling_smote, k_neighbors=30)
        under = RandomUnderSampler(sampling_strategy=0.75)
        steps = [('o', over), ('u', under)]
        pipeline = Pipeline(steps=steps)
        X_innerCV, y_innerCV = pipeline.fit_resample(X_innerCV, y_innerCV)
    
    # Hyperparameter tuning with halvingRandomSearchCV
    p_grid = {
            'max_depth': [randint(10,20)],
            'max_features': [randint(40,50)],
            'min_samples_leaf': [5,6,7,8,9,10,11,12,13],
            'min_samples_split': [4,5,6,7,8,9,10,11,12,13],
            'n_estimators':[100, 200, 300, 400, 500],
            'bootstrap': [False,True],
            'oob_score': [False],
            'random_state': [42],
            'criterion': ['gini', 'entropy'],
            'n_jobs': [-1],
            'class_weight' : [None, 'balanced']
                      }
    rand_search = HalvingRandomSearchCV(estimator=rf, param_distributions=p_grid, factor=3, random_state=42, n_jobs=-1, verbose=2, cv=cv, n_candidates=500)
    rand_search.fit(X_innerCV, y_innerCV)
    print("best sets of parameters:\n{}\n".format(rand_search.best_params_))
    
    
    # use the best estimator and fit it to the DS it was trained on and then predict the DS for outer validation
    clf = rand_search.best_estimator_
    clf.fit(X_innerCV,y_innerCV)
    
    # predict inner Cross-Validation set to checm overfitting
    y_inner_pred = clf.predict(X_innerCV).flatten()
    y_inner_prob = clf.predict_proba(X_innerCV)#[:,1]
    
    # predict outer Cross-Validation set to check for the model performance on unseen data
    y_pred = clf.predict(X_outerCV).flatten()
    y_prob = clf.predict_proba(X_outerCV)#[:,1]
    
    
    # append the inner predictions and the true values to the output-lists
    inner_true.append(y_innerCV)
    inner_pred.append(y_inner_pred)
    inner_prob.append(y_inner_prob)

    # append the outer predictions and the true values to the output-lists
    outer_true.append(y_outerCV)
    outer_pred.append(y_pred)
    outer_prob.append(y_prob)


# In[84]:


# %%time 

# evaluate the model und the training phase
evaluate_training(inner_true,inner_pred,inner_prob)
evaluate_model(outer_true,outer_pred,outer_prob)


# Quellen:
# - https://stats.stackexchange.com/questions/186337/average-roc-for-repeated-10-fold-cross-validation-with-probability-estimates
# - https://towardsdatascience.com/hyperparameter-tuning-the-random-forest-in-python-using-scikit-learn-28d2aa77dd74
# - http://scikit-learn.org/stable/auto_examples/model_selection/plot_nested_cross_validation_iris.html
# - https://machinelearningmastery.com/nested-cross-validation-for-machine-learning-with-python/
# - https://www.google.com/search?q=nested+cross+validation+sklearn&oq=nested+cross+validation+sklearn&aqs=chrome..69i57j0i22i30l5.17640j1j9&sourceid=chrome&ie=UTF-8
