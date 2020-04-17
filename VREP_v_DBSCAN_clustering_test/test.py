#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 23:47:12 2019

@author: João Gabriel Fernandes Zenóbio and Clara Loris de Sales Gomes

"""

import time
import plotly.express as px
import pandas as pd
from sklearn.cluster import DBSCAN

try:
    import sim
except:
    print("--------------------------------------------------------------")
    print("'sim.py' could not be imported. This means very probably that")
    print("either 'sim.py' or the remoteApi library could not be found.")
    print("Make sure both are in the same folder as this file,")
    print("or appropriately adjust the file 'sim.py'")
    print("--------------------------------------------------------------")
    print("")

print("Program started")
sim.simxFinish(-1)
clientID = sim.simxStart('127.0.0.1', 19999, True, True, 5000, 5)

if clientID != -1:
    print("Connected to remote API server")

    error, pioneerHandle = sim.simxGetObjectHandle(clientID, 'Pioneer_p3dx', sim.simx_opmode_oneshot_wait)
    if error == sim.simx_return_timeout_flag:
        print(str(error) + '! ERROR: simxGetObjectHandle pioneer')
    error, leftMotorHandle = sim.simxGetObjectHandle(clientID, 'Pioneer_p3dx_leftMotor', sim.simx_opmode_oneshot_wait)
    if error == sim.simx_return_timeout_flag:
        print(str(error) + '! ERROR: simxGetObjectHandle leftMotorHandle')
    error, rightMotorHandle = sim.simxGetObjectHandle(clientID, 'Pioneer_p3dx_rightMotor', sim.simx_opmode_oneshot_wait)
    if error == sim.simx_return_timeout_flag:
        print(str(error) + '! ERROR: simxGetObjectHandle rightMotorHandle')
    error, casterFreeHandle = sim.simxGetObjectHandle(clientID, 'Pioneer_p3dx_caster_freeJoint1', sim.simx_opmode_oneshot_wait)
    if error == sim.simx_return_timeout_flag:
        print(str(error) + '! ERROR: simxGetObjectHandle casterFreeHandle')

    error = sim.simxSetModelProperty(clientID, pioneerHandle, sim.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot)
    if error == sim.simx_return_ok:
        print(str(error) + '! ERROR: simxSetModelProperty pioneer')
    error = sim.simxSetModelProperty(clientID, leftMotorHandle, sim.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot)
    if error == sim.simx_return_ok:
        print(str(error) + '! ERROR: simxSetModelProperty leftMotorHandle')
    error = sim.simxSetModelProperty(clientID, rightMotorHandle, sim.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot)
    if error == sim.simx_return_ok:
        print(str(error) + '! ERROR: simxSetModelProperty rightMotorHandle')
    error = sim.simxSetModelProperty(clientID, casterFreeHandle, sim.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot)
    if error == sim.simx_return_ok:
        print(str(error) + '! ERROR: simxSetModelProperty casterFreeHandle')

    error = sim.simxSetObjectPosition(clientID, pioneerHandle, -1, (-6.5, -12, 1), sim.simx_opmode_oneshot_wait)
    if error != sim.simx_return_ok:
        print(str(error) + '! ERROR: simxSetObjectPosition pioneer')

    error = sim.simxSetModelProperty(clientID, pioneerHandle, not sim.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot)
    if error != sim.simx_return_ok:
        print(str(error) + '! ERROR: simxSetModelProperty pioneer')
    error = sim.simxSetModelProperty(clientID, leftMotorHandle, not sim.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot)
    if error != sim.simx_return_ok:
        print(str(error) + '! ERROR: simxSetModelProperty leftMotorHandle')
    error = sim.simxSetModelProperty(clientID, rightMotorHandle, not sim.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot)
    if error != sim.simx_return_ok:
        print(str(error) + '! ERROR: simxSetModelProperty rightMotorHandle')
    error = sim.simxSetModelProperty(clientID, casterFreeHandle, not sim.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot)
    if error != sim.simx_return_ok:
        print(str(error) + '! ERROR: simxSetModelProperty casterFreeHandle')

    vLeft = 3
    vRight = 3

    error = sim.simxSetJointTargetVelocity(clientID, leftMotorHandle, vLeft, sim.simx_opmode_streaming)
    if error == sim.simx_return_remote_error_flag:
        print(str(error) + '! ERROR: simxSetJointTargetVelocity left motor')
    error = sim.simxSetJointTargetVelocity(clientID, rightMotorHandle, vRight, sim.simx_opmode_streaming)
    if error == sim.simx_return_remote_error_flag:
        print(str(error) + '! ERROR: simxSetJointTargetVelocity right motor')

    error, signalValue = sim.simxGetStringSignal(clientID, "measuredDataAtThisTime", sim.simx_opmode_streaming)
    if error == sim.simx_return_remote_error_flag:
        print(str(error) + "! signalValue_streaming")
    error, signalValue = sim.simxGetStringSignal(clientID, "measuredDataAtThisTime", sim.simx_opmode_buffer)
    if error == sim.simx_return_novalue_flag:
        print(str(error) + "! signalValue_buffer")
    data = sim.simxUnpackFloats(signalValue)
    time.sleep(0.1)

    dataComplete = []
    counter = 0
    while sim.simxGetConnectionId(clientID) != -1:
        error, signalValue = sim.simxGetStringSignal(clientID, "measuredDataAtThisTime", sim.simx_opmode_buffer)
        if error == sim.simx_return_novalue_flag:
            print(str(error) + "! signalValue_buffer")
        data = sim.simxUnpackFloats(signalValue)
        dataList = []
        for i in range(0, int(len(data)), 3):
            dataList.append(data[i+1])
        if len(dataList) != 0:
            dataComplete.append(dataList)
            counter += 1
        if dataList[0] > 1:
            vLeft = 3
            vRight = 3.1
        if dataList[0] < 1:
            vLeft = 3.1
            vRight = 3
        error = sim.simxSetJointTargetVelocity(clientID, leftMotorHandle, vLeft, sim.simx_opmode_streaming)
        if error == sim.simx_return_remote_error_flag:
            print(str(error) + '! ERROR: simxSetJointTargetVelocity left motor')
        error = sim.simxSetJointTargetVelocity(clientID, rightMotorHandle, vRight, sim.simx_opmode_streaming)
        if error == sim.simx_return_remote_error_flag:
            print(str(error) + '! ERROR: simxSetJointTargetVelocity right motor')
        time.sleep(0.1)

    # Before closing the connection to V-REP, make sure that the last command sent out had time to arrive. You can guarantee this with (for example):
    sim.simxGetPingTime(clientID)
    sim.simxFinish(clientID)

    df = pd.DataFrame(dataComplete)
    df.index.name = 'object'
    label = input("Label: ")
    df['label'] = [label] * len(df)
    df.columns = df.columns.astype(str)

    try:
        db = pd.read_csv('db.csv', index_col='object')
        db = db.append(df, ignore_index=True)
        db.index.name = 'object'
        db.to_csv('db.csv')
    except FileNotFoundError:
        df.to_csv('db.csv')

else:
    print("Failed connecting to remote API server")
    print("Program ended")
