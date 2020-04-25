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

	pioneer.set_orientation()
	pioneer.set_position()

	vLeft = 3
	vRight = 3
	pioneer.set_joints_velocity()

	pioneer.check_self_simx_opmode_streaming_FLAG()

	dataComplete = []
	collectingPositionList = {"route0": [(0, 0, 90), (-6.5, -12), (-6.5, -8.6), 'route0'], "route1": [(0, 0, 90), (-3.5, -10.5), (-3.5, -8.6), 'route1'], "route2": [(0, 0, 90), (+2, -10.5), (+2, -8.6), 'route2'], "route3": [(0, 0, 90), (+6.5, -10.5), (+6.5, -8.6), 'route3'], "route4": [(0, 0, 90), (-6.5, -6), (-6.5, -1), 'route4'], "route5": [(0, 0, 90), (-3.5, -6), (-3.5, -1), 'route5'], "route6": [(0, 0, 90), (+2, -6), (+2, -1), 'route6'], "route7": [(0, 0, 90), (+6.5, -6), (+6.5, -1), 'route7'], "route8": [(0, 0, 0), (-3, 1.5), (-0.5, 1.5), 'route8'], "route9": [(0, 0, 0), (-3, -6.5), (-0.5, -6.5), 'route9'], "route10": [(0, 0, 0), (-3, -11.5), (-0.5, -11.5), 'route10'], "route11": [(0, 0, 0), (1.8, 1.5), (3.5, 1.5), 'route11'], "route12": [(0, 0, 0), (1.8, -6.5), (3.5, -6.5), 'route12'], "route13": [(0, 0, 0), (1.8, -11.5), (3.5, -11.5), 'route13']}
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
			xf = collectingPositionList["route" + str(collectingPositionListCounter)][2][0]
			yf = collectingPositionList["route" + str(collectingPositionListCounter)][2][1]
			if(((xf - x)**2 + (yf - y)**2)**0.5) < 0.1:
				label = collectingPositionList["route" + str(collectingPositionListCounter)][3]
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
				if collectingPositionListCounter > len(list(collectingPositionList.keys())):
					pioneer.close_connection_to_server()
					break
				xn = collectingPositionList["route" + str(collectingPositionListCounter)][1][0]
				yn = collectingPositionList["route" + str(collectingPositionListCounter)][1][1]
				pioneer.set_position(xn, yn)
				an = collectingPositionList["route" + str(collectingPositionListCounter)][0][0]
				bn = collectingPositionList["route" + str(collectingPositionListCounter)][0][1]
				gn = collectingPositionList["route" + str(collectingPositionListCounter)][0][2]
				pioneer.set_orientation(an, bn, gn)

else:
	print("Failed connecting to remote API server")
	print("Program ended")
