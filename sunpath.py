# Data handling and processing
import pandas as pd
import numpy as np

# Solar position calculations
from pvlib import solarposition

# Display
import plotly.express as px
import plotly.graph_objects as go
from IPython.display import display, Image
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import matplotlib.dates as mdates
import seaborn as sns

# Define the start and end dates, considering a whole year
start = f'2024-01-01 00:00:00'
end = f'2024-12-31 23:59:59'

# Generate a sequence of datetimes in 15 minutes intervals
times = pd.date_range(start, end, freq='15min')

# Calculate solar position for the daterange generated (coordinate for Peniche) 
df = solarposition.get_solarposition(times, latitude=39.34883424, longitude=-9.34298515)

# Calculate the cartesian angle
df['theta'] = 90 - df['azimuth']

# It is easy to extract datetime information
df['month'] = df.index.month
df['month_name'] = df.index.month_name()
df['day'] = df.index.day
df['time'] = df.index.time
df['minute'] = df.index.minute
df['hour'] = df.index.hour
df['dayofyear'] = df.index.dayofyear
df['date'] = pd.to_datetime(df.index.date)

# Setup the solar path dome coordinates
RADIUS = 1
df['x'] = RADIUS * np.sin(df['apparent_zenith']*np.pi/180) * np.cos(df['theta']*np.pi/180)
df['y'] = RADIUS * np.sin(df['apparent_zenith']*np.pi/180) * np.sin(df['theta']*np.pi/180)
df['z'] = RADIUS * np.cos(df['apparent_zenith']*np.pi/180)

# Setup the dome animation

# Simulation 1
# fig = px.line_3d(df, x='x', y='y', z='z', hover_name='time', animation_frame='dayofyear')

# Simulation 2
# fig = px.line_3d(df[df['day']==21], x='x', y='y', z='z', hover_name='time', color='month')

# Simulation 3
# fig = px.line_3d(df[df['day']==21], x='x', y='y', z='z', color='month')
# fig2 = px.line_3d(df[df['minute']==0], x='x', y='y', z='z', color='time')
# fig.add_traces(list(fig2.select_traces()))

# fig.update_layout(
#     scene = dict(
#         xaxis = dict(range=[-2,2],),
#         yaxis = dict(range=[-2,2],),
#         zaxis = dict(range=[-2,2],),
#         aspectratio=dict(x=1, y=1, z=1)
#     ),
# )
# fig.show()

fig, ax = plt.subplots()

sns.lineplot(data=df[(df['day']==21) & (df['month'].isin([1,2,3,4,5,6]))], x="azimuth", y="apparent_elevation", hue="month_name", color='red', ax=ax)
sns.lineplot(data=df[df['minute']==0], x="azimuth", y="apparent_elevation", hue="time", color='blue', sort=False, ax=ax)
ax.get_legend().remove()
plt.grid()
plt.show()



