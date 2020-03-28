#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 23:47:12 2019

@author: João Gabriel Fernandes Zenóbio e Clara Loris de Sales Gomes
"""

import datetime
import time
import json

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
        print(str(error) + '! ERROR: simxGetObjectHandle motor esquerdo')

    error, rightMotorHandle = vrep.simxGetObjectHandle(clientID, 'Pioneer_p3dx_rightMotor', vrep.simx_opmode_oneshot_wait)
    if error == vrep.simx_return_timeout_flag:
        print(str(error) + '! ERROR: simxGetObjectHandle motor direito')

    error = vrep.simxSetJointTargetVelocity(clientID, leftMotorHandle, vLeft, vrep.simx_opmode_streaming)
    if error == vrep.simx_return_remote_error_flag:
        print(str(error) + '! ERROR: simxSetJointTargetVelocity motor esquerdo')

    error = vrep.simxSetJointTargetVelocity(clientID, rightMotorHandle, vRight, vrep.simx_opmode_streaming)
    if error == vrep.simx_return_remote_error_flag:
        print(str(error) + '! ERROR: simxSetJointTargetVelocity motor direito')

    error, signalValue = vrep.simxGetStringSignal(clientID, 'measuredDataAtThisTime', vrep.simx_opmode_streaming)
    if error == vrep.simx_return_remote_error_flag:
        print(str(error) + '! signalValue_streaming')
    error, signalValue = vrep.simxGetStringSignal(clientID, 'measuredDataAtThisTime', vrep.simx_opmode_buffer)
    if error == vrep.simx_return_novalue_flag:
        print(str(error) + '! signalValue_buffer')
    data = vrep.simxUnpackFloats(signalValue)
    time.sleep(0.1)

    today = datetime.date.today()
    date = "_" + str(today.day) + "_" + str(today.month) + "_" + str(today.year)
    file = open("dados" + date + ".json", "w+")

    dataDict = dict()
    dataList = dict()
    dataList['data'] = []

    while vrep.simxGetConnectionId(clientID) != -1:
        error, signalValue = vrep.simxGetStringSignal(clientID, 'measuredDataAtThisTime', vrep.simx_opmode_buffer)
        if error == vrep.simx_return_novalue_flag:
            print(str(error) + '! signalValue_buffer')
        data = vrep.simxUnpackFloats(signalValue)
        for i in range(0, int(len(data)), 3):
            dataDict[str(int(i/3))] = data[i]
        dataList['data'].append(dataDict)
        time.sleep(2)

    jsonData = json.dumps(dataList, indent=4, separators=(',', ': '))
    file.write(jsonData)
    file.close()

    # Before closing the connection to V-REP, make sure that the last command sent out had time to arrive. You can guarantee this with (for example):
    vrep.simxGetPingTime(clientID)
    vrep.simxFinish(clientID)

else:
    print('Failed connecting to remote API server')
    print('Program ended')
