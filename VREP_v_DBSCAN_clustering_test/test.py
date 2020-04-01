#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 23:47:12 2019

@author: João Gabriel Fernandes Zenóbio and Clara Loris de Sales Gomes

"""

import time
import plotly.express as px
import pandas as pd
import datetime
from sklearn.cluster import DBSCAN

try:
    import vrep
except:
    print('--------------------------------------------------------------')
    print('"vrep.py" could not be imported. This means very probably that')
    print('either "vrep.py" or the remoteApi library could not be found.')
    print('Make sure both are in the same folder as this file,')
    print('or appropriately adjust the file "vrep.py"')
    print('--------------------------------------------------------------')
    print('')

print('Program started')
vrep.simxFinish(-1)
clientID = vrep.simxStart('127.0.0.1', 19999, True, True, 5000, 5)

if clientID != -1:
    print('Connected to remote API server')

    vLeft = 40
    vRight = 40
    error, leftMotorHandle = vrep.simxGetObjectHandle(clientID, 'Pioneer_p3dx_leftMotor', vrep.simx_opmode_oneshot_wait)
    if error == vrep.simx_return_timeout_flag:
        print(str(error) + '! ERROR: simxGetObjectHandle left motor')
    error, rightMotorHandle = vrep.simxGetObjectHandle(clientID, 'Pioneer_p3dx_rightMotor', vrep.simx_opmode_oneshot_wait)
    if error == vrep.simx_return_timeout_flag:
        print(str(error) + '! ERROR: simxGetObjectHandle right motor')
    error = vrep.simxSetJointTargetVelocity(clientID, leftMotorHandle, vLeft, vrep.simx_opmode_streaming)
    if error == vrep.simx_return_remote_error_flag:
        print(str(error) + '! ERROR: simxSetJointTargetVelocity left motor')
    error = vrep.simxSetJointTargetVelocity(clientID, rightMotorHandle, vRight, vrep.simx_opmode_streaming)
    if error == vrep.simx_return_remote_error_flag:
        print(str(error) + '! ERROR: simxSetJointTargetVelocity right motor')

    error, signalValue = vrep.simxGetStringSignal(clientID, 'measuredDataAtThisTime', vrep.simx_opmode_streaming)
    if error == vrep.simx_return_remote_error_flag:
        print(str(error) + '! signalValue_streaming')
    error, signalValue = vrep.simxGetStringSignal(clientID, 'measuredDataAtThisTime', vrep.simx_opmode_buffer)
    if error == vrep.simx_return_novalue_flag:
        print(str(error) + '! signalValue_buffer')
    data = vrep.simxUnpackFloats(signalValue)
    time.sleep(0.1)

    dataComplete = []
    counter = 0
    while vrep.simxGetConnectionId(clientID) != -1:
        error, signalValue = vrep.simxGetStringSignal(clientID, 'measuredDataAtThisTime', vrep.simx_opmode_buffer)
        if error == vrep.simx_return_novalue_flag:
            print(str(error) + '! signalValue_buffer')
        data = vrep.simxUnpackFloats(signalValue)
        dataList = []
        for i in range(0, int(len(data)), 3):
            dataList.append(data[i+1])
        if len(dataList) != 0:
            dataComplete.append(dataList)
            counter += 1
        time.sleep(2)

    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute
    second = now.second
    now = str(year) + "_" + str(month) + "_" + str(day) + "_" + str(hour) + "_" + str(minute) + "_" + str(second)

    df = pd.DataFrame(index=None)
    for i in range(len(dataComplete)):
        df[str(i)] = dataComplete[i]
    df.to_csv("data_" + now + ".csv")

    # Before closing the connection to V-REP, make sure that the last command sent out had time to arrive. You can guarantee this with (for example):
    vrep.simxGetPingTime(clientID)
    vrep.simxFinish(clientID)

    for i in list(df.columns):
        column = df.drop(columns=[str(i)])
        db = DBSCAN(eps=3, min_samples=5).fit(column)
        df["labels" + str(i)] = db.labels_

    fig = px.scatter(df, y='0', color="labels0")
    fig.for_each_trace(lambda trace: trace.update(name=trace.name.replace("=", ": ")),)
    fig.show()

else:
    print('Failed connecting to remote API server')
    print('Program ended')

# TODO: manter a distancia dos pontos 0 e 181 constantes para manter o robo em linha reta.
# TODO: usar o csv com as distancia para calcular a posicao dos pontos detectados por cada feixe do sensor
#  utilizando um triangulo onde a distancia é a hipotenusa e o ponto 0 ou 181 é o cateto adjascente.
