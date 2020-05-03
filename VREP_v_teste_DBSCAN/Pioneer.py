#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 23:47:12 2019

@author: João Gabriel Fernandes Zenóbio and Clara Loris de Sales Gomes

"""

try:
	import sim
	import time
	import pandas as pd
	import math
except ModuleNotFoundError:
	print("--------------------------------------------------------------")
	print("'sim.py' could not be imported. This means very probably that")
	print("either 'sim.py' or the remoteApi library could not be found.")
	print("Make sure both are in the same folder as this file,")
	print("or appropriately adjust the file 'sim.py'")
	print("--------------------------------------------------------------")
	print("")


class Pioneer:

	simxOpmodeStreamingToBuffer_FLAG = 0

	def connect_to_server(self, address='127.0.0.1', port=19999, waitUntilConnected=True, notReconnectOnceDisconnected=True, timeOutMs=5000, commThreadCycleMs=5):
		sim.simxFinish(-1)
		self.clientId = sim.simxStart(address, port, waitUntilConnected, notReconnectOnceDisconnected, timeOutMs, commThreadCycleMs)

	def close_connection_to_server(self):
		sim.simxGetPingTime(self.clientId)
		error = sim.simxStopSimulation(self.clientId, sim.simx_opmode_oneshot)
		if error == sim.simx_return_ok:
			print(str(error) + '! ERROR: simxSetModelProperty pioneer')
		sim.simxFinish(self.clientId)

	def check_server_connection(self):
		return sim.simxGetConnectionId(self.clientId) != -1

	def __init__(self):
		self.connect_to_server()
		error, self.pioneerHandle = sim.simxGetObjectHandle(self.clientId, 'Pioneer_p3dx', sim.simx_opmode_oneshot_wait)
		if error == sim.simx_return_timeout_flag:
			print(str(error) + '! ERROR: simxGetObjectHandle pioneer')
		error, self.leftMotorHandle = sim.simxGetObjectHandle(self.clientId, 'Pioneer_p3dx_leftMotor', sim.simx_opmode_oneshot_wait)
		if error == sim.simx_return_timeout_flag:
			print(str(error) + '! ERROR: simxGetObjectHandle self.leftMotorHandle')
		error, self.rightMotorHandle = sim.simxGetObjectHandle(self.clientId, 'Pioneer_p3dx_rightMotor', sim.simx_opmode_oneshot_wait)
		if error == sim.simx_return_timeout_flag:
			print(str(error) + '! ERROR: simxGetObjectHandle self.rightMotorHandle')
		error, self.casterFreeHandle = sim.simxGetObjectHandle(self.clientId, 'Pioneer_p3dx_caster_freeJoint1', sim.simx_opmode_oneshot_wait)
		if error == sim.simx_return_timeout_flag:
			print(str(error) + '! ERROR: simxGetObjectHandle self.casterFreeHandle')

	def check_self_simx_opmode_streaming_FLAG(self):
		if self.simxOpmodeStreamingToBuffer_FLAG == 0:
			error, signalValue = sim.simxGetStringSignal(self.clientId, "measuredDataAtThisTime", sim.simx_opmode_streaming)
			if error == sim.simx_return_remote_error_flag:
				print(str(error) + "! simxGetStringSignal_streaming")
			error, signalValue = sim.simxGetStringSignal(self.clientId, "measuredDataAtThisTime", sim.simx_opmode_buffer)
			if error == sim.simx_return_novalue_flag:
				print(str(error) + "! simxGetStringSignal_buffer")
			sim.simxUnpackFloats(signalValue)
			error, position = sim.simxGetObjectPosition(self.clientId, self.pioneerHandle, -1, sim.simx_opmode_streaming)
			if error == sim.simx_return_remote_error_flag:
				print(str(error) + "! simxGetObjectPosition_streaming")
			error, position = sim.simxGetObjectPosition(self.clientId, self.pioneerHandle, -1, sim.simx_opmode_buffer)
			if error == sim.simx_return_novalue_flag:
				print(str(error) + "! simxGetObjectPosition_buffer")
			self.simxOpmodeStreamingToBuffer_FLAG = 1
			time.sleep(0.1)

	def set_position(self, x=-7, y=-12, z=0.3):
		error = sim.simxSetModelProperty(self.clientId, self.pioneerHandle, sim.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot)
		if error != sim.simx_return_ok:
			print(str(error) + '! ERROR: simxSetModelProperty pioneer')
		error = sim.simxSetModelProperty(self.clientId, self.leftMotorHandle, sim.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot)
		if error != sim.simx_return_ok:
			print(str(error) + '! ERROR: simxSetModelProperty self.leftMotorHandle')
		error = sim.simxSetModelProperty(self.clientId, self.rightMotorHandle, sim.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot)
		if error != sim.simx_return_ok:
			print(str(error) + '! ERROR: simxSetModelProperty self.rightMotorHandle')
		error = sim.simxSetModelProperty(self.clientId, self.casterFreeHandle, sim.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot)
		if error != sim.simx_return_ok:
			print(str(error) + '! ERROR: simxSetModelProperty self.casterFreeHandle')

		error = sim.simxSetObjectPosition(self.clientId, self.pioneerHandle, -1, (x, y, z), sim.simx_opmode_oneshot_wait)
		if error != sim.simx_return_ok:
			print(str(error) + '! ERROR: simxSetObjectPosition pioneer')

		error = sim.simxSetModelProperty(self.clientId, self.pioneerHandle, not sim.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot)
		if error != sim.simx_return_ok:
			print(str(error) + '! ERROR: simxSetModelProperty pioneer')
		error = sim.simxSetModelProperty(self.clientId, self.leftMotorHandle, not sim.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot)
		if error != sim.simx_return_ok:
			print(str(error) + '! ERROR: simxSetModelProperty self.leftMotorHandle')
		error = sim.simxSetModelProperty(self.clientId, self.rightMotorHandle, not sim.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot)
		if error != sim.simx_return_ok:
			print(str(error) + '! ERROR: simxSetModelProperty self.rightMotorHandle')
		error = sim.simxSetModelProperty(self.clientId, self.casterFreeHandle, not sim.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot)
		if error != sim.simx_return_ok:
			print(str(error) + '! ERROR: simxSetModelProperty self.casterFreeHandle')

	def get_position(self):
		error, position = sim.simxGetObjectPosition(self.clientId, self.pioneerHandle, -1, sim.simx_opmode_buffer)
		if error == sim.simx_return_novalue_flag:
				print(str(error) + "! simxGetObjectPosition_buffer")
		return position

	def set_orientation(self, a=0, b=0, g=90):
		a = math.radians(a)
		b = math.radians(b)
		g = math.radians(g)
		error = sim.simxSetModelProperty(self.clientId, self.pioneerHandle, sim.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot)
		if error != sim.simx_return_ok:
			print(str(error) + '! ERROR: simxSetModelProperty pioneer')
		error = sim.simxSetModelProperty(self.clientId, self.leftMotorHandle, sim.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot)
		if error != sim.simx_return_ok:
			print(str(error) + '! ERROR: simxSetModelProperty self.leftMotorHandle')
		error = sim.simxSetModelProperty(self.clientId, self.rightMotorHandle, sim.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot)
		if error != sim.simx_return_ok:
			print(str(error) + '! ERROR: simxSetModelProperty self.rightMotorHandle')
		error = sim.simxSetModelProperty(self.clientId, self.casterFreeHandle, sim.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot)
		if error != sim.simx_return_ok:
			print(str(error) + '! ERROR: simxSetModelProperty self.casterFreeHandle')

		error = sim.simxSetObjectOrientation(self.clientId, self.pioneerHandle, -1, (a, b, g), sim.simx_opmode_oneshot_wait)
		if error != sim.simx_return_ok:
			print(str(error) + '! ERROR: simxSetObjectPosition pioneer')
		time.sleep(0.1)

		error = sim.simxSetModelProperty(self.clientId, self.pioneerHandle, not sim.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot)
		if error != sim.simx_return_ok:
			print(str(error) + '! ERROR: simxSetModelProperty pioneer')
		error = sim.simxSetModelProperty(self.clientId, self.leftMotorHandle, not sim.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot)
		if error != sim.simx_return_ok:
			print(str(error) + '! ERROR: simxSetModelProperty self.leftMotorHandle')
		error = sim.simxSetModelProperty(self.clientId, self.rightMotorHandle, not sim.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot)
		if error != sim.simx_return_ok:
			print(str(error) + '! ERROR: simxSetModelProperty self.rightMotorHandle')
		error = sim.simxSetModelProperty(self.clientId, self.casterFreeHandle, not sim.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot)
		if error != sim.simx_return_ok:
			print(str(error) + '! ERROR: simxSetModelProperty self.casterFreeHandle')

	def set_joints_velocity(self, left_motor_velocity=3, right_motor_velocity=3):
		error = sim.simxSetJointTargetVelocity(self.clientId, self.leftMotorHandle, left_motor_velocity, sim.simx_opmode_streaming)
		if error == sim.simx_return_remote_error_flag:
			print(str(error) + '! ERROR: simxSetJointTargetVelocity left motor')
		error = sim.simxSetJointTargetVelocity(self.clientId, self.rightMotorHandle, right_motor_velocity, sim.simx_opmode_streaming)
		if error == sim.simx_return_remote_error_flag:
			print(str(error) + '! ERROR: simxSetJointTargetVelocity right motor')

	def get_laser_2d_data(self):
		error, signalValue = sim.simxGetStringSignal(self.clientId, "measuredDataAtThisTime", sim.simx_opmode_buffer)
		if error == sim.simx_return_novalue_flag:
			print(str(error) + "! signalValue_buffer")
		data = sim.simxUnpackFloats(signalValue)
		dataList = []
		for i in range(0, int(len(data)), 3):
			dataList.append(-data[i+2])
		if len(dataList) == 182:
			time.sleep(0.1)
			return dataList
		else:
			return False

