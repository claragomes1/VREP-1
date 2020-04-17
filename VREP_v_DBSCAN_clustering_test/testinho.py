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

	error = sim.simxSetObjectPosition(clientID, pioneerHandle, -1, (-6.5, -12, 3), sim.simx_opmode_oneshot_wait)
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

	# Before closing the connection to V-REP, make sure that the last command sent out had time to arrive. You can guarantee this with (for example):
	sim.simxGetPingTime(clientID)
	sim.simxFinish(clientID)

else:
	print("Failed connecting to remote API server")
	print("Program ended")
