# -*- coding: utf-8 -*-
"""DataVisualizationWithPython3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Q_BVYPbIB_Arg3uem8NcTF5rFCNHwBeN

> # **Data Visualization with Python (Part 3)**

- In this notebook, I will plot Choropleth Maps which are thematic maps in which areas are shaded or patterned in proportion to the measurement of the statistical variable being displayed on the map. The choropleth maps provide an easy way to visualize how a measurement varies across a geographic area or to show the level of variability within a region. 



- My dataset contains information about Immigration to Canada from 1980 to 2013 - International migration flows to, and from selected countries and its format is .csv. The data is hosted on United Nation's website.

- I've uploaded the dataset to Google Drive.

Let's get started!
"""

!pip install -q -U watermark

# Commented out IPython magic to ensure Python compatibility.
# %reload_ext watermark
# %watermark -v -p numpy,pandas,matplotlib

!pip install js

# Commented out IPython magic to ensure Python compatibility.
#import os
import numpy as np
import pandas as pd
#from tqdm import tqdm
#import seaborn as sns
#from pylab import rcParams
# %matplotlib inline 
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import rc
#from scipy import stats
#import matplotlib.patches as mpatches
#from PIL import Image
import folium
import io
import json

from google.colab import drive
drive.mount('/content/gdrive')

!ls '/content/gdrive'

df = pd.read_csv('/content/gdrive/MyDrive/canada.csv',encoding = "ISO-8859-1")
df.head(2)

df.shape

""">**Cleaning up data**"""

#In pandas axis=0 represents rows (default) and axis=1 represents columns.

df.drop(['AREA','REG','DEV','Type','Coverage'], axis=1, inplace=True)

df.rename(columns={'OdName':'Country', 'AreaName':'Continent', 'RegName':'Region'}, inplace=True)

df.columns = list(map(str, df.columns))

df['Total'] = df.sum(axis=1)

years = list(map(str, range(1980, 2014)))
print('data dimensions:', df.shape)

df.head()

"""> **Findig Missing Values**"""

df.replace("?", np.NAN, inplace = True)
df.replace("*", np.NAN, inplace = True)


missing_data = df.isnull()
missing_data.tail()

for column in missing_data.columns.values.tolist():
    print(column)
    print (missing_data[column].value_counts())
    print("")

"""- Based on the summary above, our data does not have any missing value.

> In this step, I need a GeoJSON file that defines the areas/boundaries of the state, and county.
"""

myfile = open('/content/gdrive/MyDrive/world_countries.json') # open JSON file
world_geo = json.load(myfile) # load JSON file into world_geo (JSON file conains borders of the countries)
json.dumps(world_geo, indent=4) # show me the JSON file details; first 4 rows

"""I will apply the choropleth method with the following main parameters to create a Choropleth map:

- geo_data, which is the GeoJSON file.
- data, which is the dataframe containing the data.
- columns, which represents the columns in the dataframe that will be used to create the Choropleth map.
- key_on, which is the key or variable in the GeoJSON file that contains the name of the variable of interest.
"""

#Before starting this section I must get the dataset of the top 15 countries based on the Total immigrant population.
#Name the dataframe df_top15.
df_top15 = df.sort_values(['Total'], ascending=False, axis=0).head(15)
df_top15

# create a numpy array of length 6 and has linear spacing from the minimum total immigration to the maximum total immigration
threshold_scale = np.linspace(df['Total'].min(),
                              df['Total'].max(),
                              6, dtype=int)
threshold_scale = threshold_scale.tolist() # change the numpy array to a list
threshold_scale[-1] = threshold_scale[-1] + 1 # make sure that the last value of the list is greater than the maximum immigration

# let Folium determine the scale.
world_map = folium.Map(location=[0, 0], zoom_start=2)
world_map.choropleth(
    geo_data=world_geo,
    data=df,
    columns=['Country', 'Total'],
    key_on='feature.properties.name',
    threshold_scale=threshold_scale,
    fill_color='YlOrRd', 
    fill_opacity=0.7, 
    line_opacity=0.2,
    legend_name='Immigration to Canada',
    reset=True
)
world_map

"""As per the Choropleth map legend, the darker the color of a country and the closer the color to red, the higher the number of immigrants from that country. Accordingly, the highest immigration over the course of 33 years (from 1980 to 2013) was from China, India, and the Philippines, followed by Poland, Pakistan, and interestingly, the US.

> I am going to create Choropleth map for 1995 and compare it with the entire period from 1980 to 2013.
"""

#Name the dataframe df_top15 in 1995
df_top15 = df.sort_values(['1995'], ascending=False, axis=0).head(15)
df_top15

# create a numpy array of length 6 and has linear spacing from the minimum total immigration to the maximum total immigration
threshold_scale = np.linspace(df['1995'].min(),
                              df['1995'].max(),
                              6, dtype=int)
threshold_scale = threshold_scale.tolist() # change the numpy array to a list
threshold_scale[-1] = threshold_scale[-1] + 1 # make sure that the last value of the list is greater than the maximum immigration

# let Folium determine the scale.
world_map = folium.Map(location=[0, 0], zoom_start=2)
world_map.choropleth(
    geo_data=world_geo,
    data=df,
    columns=['Country', '1995'],
    key_on='feature.properties.name',
    threshold_scale=threshold_scale,
    fill_color='YlOrRd', 
    fill_opacity=0.7, 
    line_opacity=0.2,
    legend_name='Immigration to Canada',
    reset=True
)
world_map