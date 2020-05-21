#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 23:47:12 2019

@author: João Gabriel Fernandes Zenóbio and Clara Loris de Sales Gomes

"""

import time
import json
import plotly.graph_objects as go
import pandas as pd
import datetime

try:
    import sim
except:
    print('--------------------------------------------------------------')
    print('"sim.py" could not be imported. This means very probably that')
    print('either "sim.py" or the remoteApi library could not be found.')
    print('Make sure both are in the same folder as this file,')
    print('or appropriately adjust the file "sim.py"')
    print('--------------------------------------------------------------')
    print('')

print('Program started')
sim.simxFinish(-1)
clientID = sim.simxStart('127.0.0.1', 19999, True, True, 5000, 5)

if clientID != -1:
    print('Connected to remote API server')

    error, signalValue = sim.simxGetStringSignal(clientID, 'measuredDataAtThisTime', sim.simx_opmode_streaming)
    if error == sim.simx_return_remote_error_flag:
        print(str(error) + '! signalValue_streaming')
    error, signalValue = sim.simxGetStringSignal(clientID, 'measuredDataAtThisTime', sim.simx_opmode_buffer)
    if error == sim.simx_return_novalue_flag:
        print(str(error) + '! signalValue_buffer')
    data = sim.simxUnpackFloats(signalValue)
    time.sleep(0.1)

    dataList = dict()
    counter = 0

    while sim.simxGetConnectionId(clientID) != -1:
        error, signalValue = sim.simxGetStringSignal(clientID, 'measuredDataAtThisTime', sim.simx_opmode_buffer)
        if error == sim.simx_return_novalue_flag:
            print(str(error) + '! signalValue_buffer')
        data = sim.simxUnpackFloats(signalValue)
        dataDict = dict()
        for i in range(0, int(len(data)), 3):
            dataDict[str(int(i/3))] = data[i+1]
        dataList[str(counter)] = dataDict
        counter += 1
        time.sleep(2)
    completeData = dict()
    completeData["data"] = dataList
    jsonData = json.dumps(completeData, indent=4, separators=(',', ': '))

    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute
    second = now.second
    now = str(year) + "_" + str(month) + "_" + str(day) + "_" + str(hour) + "_" + str(minute) + "_" + str(second)
    file = open("data_" + now + ".json", "w+")
    file.write(jsonData)
    file.close()

    # Before closing the connection to V-REP, make sure that the last command sent out had time to arrive. You can guarantee this with (for example):
    sim.simxGetPingTime(clientID)
    sim.simxFinish(clientID)

    df = pd.read_json("data_" + now + ".json", "r")

    fig = go.Figure()
    for i in range(len(df.data)):
        fig.add_trace(
            go.Scatter(
                x=list(df.data[i].keys()),
                y=list(df.data[i].values())
            ))

    fig.show()

else:
    print('Failed connecting to remote API server')
    print('Program ended')
