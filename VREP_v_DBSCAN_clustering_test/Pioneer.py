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
except ModuleNotFoundError:
	print("--------------------------------------------------------------")
	print("'sim.py' could not be imported. This means very probably that")
	print("either 'sim.py' or the remoteApi library could not be found.")
	print("Make sure both are in the same folder as this file,")
	print("or appropriately adjust the file 'sim.py'")
	print("--------------------------------------------------------------")
	print("")


class Pioneer:

	simx_opmode_streaming_FLAG = 0

	def connect_to_server(self, address='127.0.0.1', port=19999, wait_until_connected=True, not_reconnect_once_disconnected=True, time_out_ms=5000, comm_thread_cycle_ms=5):
		sim.simxFinish(-1)
		self.client_id = sim.simxStart(address, port, wait_until_connected, not_reconnect_once_disconnected, time_out_ms, comm_thread_cycle_ms)

	def close_connection_to_server(self):
		sim.simxGetPingTime(self.client_id)
		sim.simxFinish(self.client_id)

	def check_server_connection(self):
		return sim.simxGetConnectionId(self.client_id) != -1

	def __init__(self):
		self.connect_to_server()
		error, self.pioneer_handle = sim.simxGetObjectHandle(self.client_id, 'Pioneer_p3dx', sim.simx_opmode_oneshot_wait)
		if error == sim.simx_return_timeout_flag:
			print(str(error) + '! ERROR: simxGetObjectHandle pioneer')
		error, self.left_motor_handle = sim.simxGetObjectHandle(self.client_id, 'Pioneer_p3dx_leftMotor', sim.simx_opmode_oneshot_wait)
		if error == sim.simx_return_timeout_flag:
			print(str(error) + '! ERROR: simxGetObjectHandle self.leftMotorHandle')
		error, self.right_motor_handle = sim.simxGetObjectHandle(self.client_id, 'Pioneer_p3dx_rightMotor', sim.simx_opmode_oneshot_wait)
		if error == sim.simx_return_timeout_flag:
			print(str(error) + '! ERROR: simxGetObjectHandle self.rightMotorHandle')
		error, self.caster_free_handle = sim.simxGetObjectHandle(self.client_id, 'Pioneer_p3dx_caster_freeJoint1', sim.simx_opmode_oneshot_wait)
		if error == sim.simx_return_timeout_flag:
			print(str(error) + '! ERROR: simxGetObjectHandle self.casterFreeHandle')

	def set_position(self, x=-6.5, y=-12, z=1):

		error = sim.simxSetModelProperty(self.client_id, self.pioneer_handle, sim.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot)
		if error == sim.simx_return_ok:
			print(str(error) + '! ERROR: simxSetModelProperty pioneer')
		error = sim.simxSetModelProperty(self.client_id, self.left_motor_handle, sim.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot)
		if error == sim.simx_return_ok:
			print(str(error) + '! ERROR: simxSetModelProperty self.leftMotorHandle')
		error = sim.simxSetModelProperty(self.client_id, self.right_motor_handle, sim.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot)
		if error == sim.simx_return_ok:
			print(str(error) + '! ERROR: simxSetModelProperty self.rightMotorHandle')
		error = sim.simxSetModelProperty(self.client_id, self.caster_free_handle, sim.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot)
		if error == sim.simx_return_ok:
			print(str(error) + '! ERROR: simxSetModelProperty self.casterFreeHandle')

		error = sim.simxSetObjectPosition(self.client_id, self.pioneer_handle, -1, (x, y, z), sim.simx_opmode_oneshot_wait)
		if error != sim.simx_return_ok:
			print(str(error) + '! ERROR: simxSetObjectPosition pioneer')

		error = sim.simxSetModelProperty(self.client_id, self.pioneer_handle, not sim.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot)
		if error != sim.simx_return_ok:
			print(str(error) + '! ERROR: simxSetModelProperty pioneer')
		error = sim.simxSetModelProperty(self.client_id, self.left_motor_handle, not sim.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot)
		if error != sim.simx_return_ok:
			print(str(error) + '! ERROR: simxSetModelProperty self.leftMotorHandle')
		error = sim.simxSetModelProperty(self.client_id, self.right_motor_handle, not sim.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot)
		if error != sim.simx_return_ok:
			print(str(error) + '! ERROR: simxSetModelProperty self.rightMotorHandle')
		error = sim.simxSetModelProperty(self.client_id, self.caster_free_handle, not sim.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot)
		if error != sim.simx_return_ok:
			print(str(error) + '! ERROR: simxSetModelProperty self.casterFreeHandle')

	def set_joints_velocity(self, left_motor_velocity=3, right_motor_velocity=3):
		error = sim.simxSetJointTargetVelocity(self.client_id, self.left_motor_handle, left_motor_velocity, sim.simx_opmode_streaming)
		if error == sim.simx_return_remote_error_flag:
			print(str(error) + '! ERROR: simxSetJointTargetVelocity left motor')
		error = sim.simxSetJointTargetVelocity(self.client_id, self.right_motor_handle, right_motor_velocity, sim.simx_opmode_streaming)
		if error == sim.simx_return_remote_error_flag:
			print(str(error) + '! ERROR: simxSetJointTargetVelocity right motor')

	def check_self_simx_opmode_streaming_FLAG(self):
		if self.simx_opmode_streaming_FLAG == 0:
			error, signalValue = sim.simxGetStringSignal(self.client_id, "measuredDataAtThisTime", sim.simx_opmode_streaming)
			if error == sim.simx_return_remote_error_flag:
				print(str(error) + "! signalValue_streaming")
			error, signalValue = sim.simxGetStringSignal(self.client_id, "measuredDataAtThisTime", sim.simx_opmode_buffer)
			if error == sim.simx_return_novalue_flag:
				print(str(error) + "! signalValue_buffer")
			sim.simxUnpackFloats(signalValue)
			self.simx_opmode_streaming_FLAG = 1
			time.sleep(0.1)

	def get_laser_2d_data(self):
		error, signalValue = sim.simxGetStringSignal(self.client_id, "measuredDataAtThisTime", sim.simx_opmode_buffer)
		if error == sim.simx_return_novalue_flag:
			print(str(error) + "! signalValue_buffer")
		data = sim.simxUnpackFloats(signalValue)
		dataList = []
		for i in range(0, int(len(data)), 3):
			dataList.append(data[i+1])
		if len(dataList) != 0:
			time.sleep(0.1)
			return dataList
