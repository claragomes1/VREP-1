import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import datetime

today = datetime.date.today()
date = "_" + str(today.day) + "_" + str(today.month) + "_" + str(today.year)
df = pd.read_json("dados" + date + ".json", "r")

fig = go.Figure()
for i in range(len(df.data)):
	fig.add_trace(
		go.Scatter(
			x=list(df.data[i].keys()),
			y=list(df.data[i].values())
		))

fig.show()
