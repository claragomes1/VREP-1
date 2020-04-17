#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 23:47:12 2019

@author: João Gabriel Fernandes Zenóbio and Clara Loris de Sales Gomes

"""
import pandas as pd
from sklearn.cluster import DBSCAN
from Pioneer import Pioneer

print("Program started")

pioneer = Pioneer()


if pioneer.client_id != -1:
	print("Connected to remote API server")

	pioneer.set_position()

	vLeft = 3
	vRight = 3
	pioneer.set_joints_velocity()

	pioneer.check_self_simx_opmode_streaming_FLAG()

	dataComplete = []
	while pioneer.check_server_connection():
		dataList = pioneer.get_laser_2d_data()
		if len(dataList) != 0:
			dataComplete.append(dataList)
		if dataList[0] > 1:
			vLeft = 3
			vRight = 3.1
		if dataList[0] < 1:
			vLeft = 3.1
			vRight = 3
		pioneer.set_joints_velocity(vLeft, vRight)

	pioneer.close_connection_to_server()

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
