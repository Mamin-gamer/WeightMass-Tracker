import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime
from matplotlib import dates as dts
from matplotlib.dates import MO

df = pd.read_csv('Data.csv', skiprows = 4, skipfooter = 6, engine='python')
df = df[~df['Muscle Mass'].str.contains('-')]
df = df[~df['Weight'].str.contains('-')]
df = df[~df['Body Fat'].str.contains('-')]
df = df.reset_index(drop = True)

df = df.replace({
                    'Weight' : '[A-Za-z]',
                    'Body Fat': '%',
                    'Muscle Mass': '%'

}, '', regex = True)


convert_dict = {'Weight': float,
                'Body Fat': float,
                'Muscle Mass': float
               }
df = df.astype(convert_dict)



df['Date'] = pd.to_datetime(pd.to_datetime(df['Date']).dt.date)

while len(df['Date'])/7 != len(df['Date'])//7:
    index = list(df['Date'].duplicated(keep = 'last')).index(True)
    df = df.drop(index)
    df = df.reset_index(drop = True)

dates = df['Date']
weight = np.array(df['Weight'])
body_fat = np.array(df['Body Fat'])
muscle_mass = np.array(df['Muscle Mass'])

muscle_max = df['Muscle Mass'].max()
muscle_min = df['Muscle Mass'].min()
muscle_max_index = list(muscle_mass).index(muscle_max)
muscle_min_index = list(muscle_mass).index(muscle_min)

fat_max = df['Body Fat'].max()
fat_min = df['Body Fat'].min()
fat_max_index = list(body_fat).index(fat_max)
fat_min_index = list(body_fat).index(fat_min)

weight_max = df['Weight'].max()
weight_min = df['Weight'].min()
weight_max_index = list(weight).index(weight_max)
weight_min_index = list(weight).index(weight_min)


actual_muscle_mass = muscle_mass/100*weight
actual_body_fat = body_fat/100*weight


dates_week = np.mean(np.array_split(dates.dt.week, len(dates)//7), axis = 1).astype(int)
muscle_median = np.median(np.array_split(muscle_mass, len(muscle_mass)//7), axis = 1)
fat_median = np.median(np.array_split(body_fat, len(body_fat)//7), axis = 1)
weight_median = np.median(np.array_split(weight, len(weight)//7), axis = 1)


fig, ax1 = plt.subplots(figsize = (10,6))
ax2 = ax1.twiny()
ax1.set_title('Weight')

ax2.plot(dates_week ,weight_median, color = 'orange', label = 'Median Weight per week')
ax1.plot(dates, weight, label = 'Weight')
ax1.scatter(np.array(dates)[weight_max_index], weight_max, label = 'Max Weight', color = 'red', s = 100, facecolors = 'none')
ax1.scatter(np.array(dates)[weight_min_index], weight_min, label = 'Min Weight', color = 'green', s = 100, facecolors = 'none')
ax2.axis('off')

handles,labels = ax1.get_legend_handles_labels()
handles1,labels1 = ax2.get_legend_handles_labels()
handles = [handles[0], handles1[0], handles[1], handles[2]]
labels = [labels[0],  labels1[0], labels[1], labels[2]]
fig.legend  (handles, labels,
            bbox_to_anchor = (0.95, 0.7),
            borderaxespad=0.3,
            title="Legend Title",
)

plt.tight_layout()
fig.autofmt_xdate()
myFmt = dts.DateFormatter("%d/%m")
ax1.xaxis.set_major_formatter(myFmt)
loc = dts.WeekdayLocator(byweekday=MO)
ax1.xaxis.set_major_locator(loc)
ax1.grid()




plt.figure(1)

fig, ax1 = plt.subplots(figsize = (10,6))
ax2 = ax1.twiny()
ax1.set_title('Muscle Mass')

ax2.plot(dates_week, muscle_median, color = 'orange', label = 'Median Weight per week')
ax1.plot(dates, muscle_mass, label = 'Weight')
ax1.scatter(np.array(dates)[muscle_max_index], muscle_max, label = 'Max Muscle %', color = 'red', s = 100, facecolors = 'none')
ax1.scatter(np.array(dates)[muscle_min_index], muscle_min, label = 'Min Muscle %', color = 'green', s = 100, facecolors = 'none')
ax2.axis('off')

handles,labels = ax1.get_legend_handles_labels()
handles1,labels1 = ax2.get_legend_handles_labels()
handles = [handles[0], handles1[0], handles[1], handles[2]]
labels = [labels[0],  labels1[0], labels[1], labels[2]]
fig.legend  (handles, labels,
            bbox_to_anchor = (0.95, 0.35),
            borderaxespad=0.3,
            title="Legend Title",
)

plt.tight_layout()
fig.autofmt_xdate()
myFmt = dts.DateFormatter("%d/%m")
ax1.xaxis.set_major_formatter(myFmt)
loc = dts.WeekdayLocator(byweekday=MO)
ax1.xaxis.set_major_locator(loc)
ax1.grid()





plt.figure(2)

fig, ax1 = plt.subplots(figsize = (10,6))
ax2 = ax1.twiny()
ax1.set_title('Body Fat')

ax2.plot(dates_week ,fat_median, color = 'orange', label = 'Median Body Fat per week')
ax1.plot(dates, body_fat, label = 'Weight')
ax1.scatter(np.array(dates)[fat_max_index], fat_max, label = 'Max Weight', color = 'red', s = 100, facecolors = 'none')
ax1.scatter(np.array(dates)[fat_min_index], fat_min, label = 'Min Weight', color = 'green', s = 100, facecolors = 'none')
ax2.axis('off')

handles,labels = ax1.get_legend_handles_labels()
handles1,labels1 = ax2.get_legend_handles_labels()
handles = [handles[0], handles1[0], handles[1], handles[2]]
labels = [labels[0],  labels1[0], labels[1], labels[2]]
fig.legend  (handles, labels,
            bbox_to_anchor = (0.95, 0.7),
            borderaxespad=0.3,
            title="Legend Title",
)


plt.tight_layout()
fig.autofmt_xdate()
myFmt = dts.DateFormatter("%d/%m")
ax1.xaxis.set_major_formatter(myFmt)

loc = dts.WeekdayLocator(byweekday=MO)
ax1.xaxis.set_major_locator(loc)

ax1.grid()



plt.figure(3)

fig, ax1 = plt.subplots(figsize = (10,6))
ax2 = ax1.twinx()
ax1.set_title('Actual Body Fat and Muscle Mass')

ax1.plot(dates, actual_body_fat, label = 'Body fat in kg', color = 'lightsalmon')
ax1.tick_params(axis = 'y', colors = 'lightsalmon')

ax2.plot(dates, actual_muscle_mass, label = 'Muscle Mass in kg', color = 'blue')
ax2.tick_params(axis = 'y', colors = 'blue')

fig.legend(title = 'Legend',
            bbox_to_anchor = (0.75, 0.8)

)
plt.tight_layout()
fig.autofmt_xdate()
myFmt = dts.DateFormatter("%d/%m")
ax1.xaxis.set_major_formatter(myFmt)

loc = dts.WeekdayLocator(byweekday=MO)
ax1.xaxis.set_major_locator(loc)

ax1.grid()





plt.show()
