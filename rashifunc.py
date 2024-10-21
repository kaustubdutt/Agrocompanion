from sklearn.ensemble import RandomForestRegressor
import os
import pickle
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import preprocessing

cwd = os.getcwd()
df_2013 = pd.read_pickle(os.path.join(cwd,'data','df_2013_clean.df'))
df_2014 = pd.read_pickle(os.path.join(cwd,'data','df_2014_clean.df'))
df_all = pd.concat([df_2013,df_2014])
def inp(long,lat,t1,dp, hum ):
    y = df_all['yield']
    X = df_all.drop('yield',axis=1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    columns_to_scale = df_all.columns.tolist()
    columns_to_scale = [x for x in columns_to_scale if x != 'yield']
    std_scaler = preprocessing.StandardScaler().fit(X_train[columns_to_scale])
    minmax_scaler = preprocessing.MinMaxScaler().fit(X_train)
    X_train[columns_to_scale] = std_scaler.transform(X_train[columns_to_scale])
    X_test[columns_to_scale] = std_scaler.transform(X_test[columns_to_scale])
    X, y = X_train, y_train
    est = RandomForestRegressor(n_estimators=100, n_jobs=-1, max_features= 'sqrt')
    est.fit(X_train, y_train)

    x_new = pd.DataFrame({'Longitude':long , 'Latitude': lat, 'temp':t1 , 'dewPoint':dp , 'humidity':hum },index =[0])
    std_scaler = preprocessing.StandardScaler().fit(x_new)
    minmax_scaler = preprocessing.MinMaxScaler().fit(x_new)
    x_new = std_scaler.transform(x_new)
    y_pred = est.predict(x_new)


    return y_pred.round(4)


# y = df_all['yield']
# X = df_all.drop('yield',axis=1)
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)
# columns_to_scale = df_all.columns.tolist()
#
# columns_to_scale = [x for x in columns_to_scale if x != 'yield']
#
# std_scaler = preprocessing.StandardScaler().fit(X_train[columns_to_scale])
# minmax_scaler = preprocessing.MinMaxScaler().fit(X_train)
#
# X_train[columns_to_scale] = std_scaler.transform(X_train[columns_to_scale])
# X_test[columns_to_scale] = std_scaler.transform(X_test[columns_to_scale])
# #MOdel
# X, y = X_train, y_train
# est = RandomForestRegressor(n_estimators=100, n_jobs=-1, max_features= 'sqrt')
# est.fit(X_train, y_train)
# #Func
# def inp(long, lat, t1, dp, hum):
#     x_new = pd.DataFrame(
#         {'Longitude': long, 'Latitude': lat, 'temp': t1, 'dewPoint': dp, 'humidity': hum},
#         index=[0])
#     std_scaler = preprocessing.StandardScaler().fit(x_new)
#     minmax_scaler = preprocessing.MinMaxScaler().fit(x_new)
#     x_new = std_scaler.transform(x_new)
#     y_pred = est.predict(x_new)
#     print(y_pred)
#     return y_pred
# #a = inp(46.9298391,46.811686,22.090000,29.563710,0.648065)
# #print(a)

