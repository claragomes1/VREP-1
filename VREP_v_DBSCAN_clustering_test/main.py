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


if pioneer.clientId != -1:
	print("Connected to remote API server")

	pioneer.set_position()

	vLeft = 3
	vRight = 3
	pioneer.set_joints_velocity()

	pioneer.check_self_simx_opmode_streaming_FLAG()

	dataComplete = []
	collectingPositionList = {"route0": [(-6.5, -12), (-6.5, -8.5), 'route0'], "route1": [(-3.5, -12), (-3.5, -8.5), 'route1'], "route2": [(-6.5, -12), (-6.5, -8.5), 'route2']}
	collectingPositionListCounter = 0
	while pioneer.check_server_connection():
		dataList = pioneer.get_laser_2d_data()
		if dataList != False:
			dataComplete.append(dataList)
			if dataList[0] > 1:
				vLeft = 3
				vRight = 3.1
			if dataList[0] < 1:
				vLeft = 3.1
				vRight = 3
			pioneer.set_joints_velocity(vLeft, vRight)
			x, y, z = pioneer.get_position()
			xf = collectingPositionList["route" + str(collectingPositionListCounter)][1][0]
			yf = collectingPositionList["route" + str(collectingPositionListCounter)][1][1]
			if(((xf - x)**2 + (yf - y)**2)**0.5) < 0.1:
				if collectingPositionListCounter > 1:
					break
				label = collectingPositionList["route" + str(collectingPositionListCounter)][2]
				df = pd.DataFrame(dataComplete)
				df.index.name = 'object'
				df['label'] = [label] * len(df)
				df.columns = df.columns.astype(str)
				try:
					db = pd.read_csv('db.csv', index_col='object')
					db = db.append(df, ignore_index=True)
					db.index.name = 'object'
					db.to_csv('db.csv')
				except FileNotFoundError:
					df.to_csv('db.csv')
				collectingPositionListCounter+=1
				xn = collectingPositionList["route" + str(collectingPositionListCounter)][0][0]
				yn = collectingPositionList["route" + str(collectingPositionListCounter)][0][1]
				pioneer.set_position(xn, yn)

	pioneer.close_connection_to_server()

else:
	print("Failed connecting to remote API server")
	print("Program ended")
