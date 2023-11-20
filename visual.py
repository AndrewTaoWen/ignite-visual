import matplotlib.pyplot as plt
import pandas as pd
import pyvis as pv
import numpy as np
from collections import Counter

#import data

data_file = "data.xlsx"
df = pd.read_excel(data_file)


df = df.drop('Name (Chinese)', axis=1)
df = df.drop('Entity owner (Chinese)', axis=1)
df = df.drop('Parent entity (Chinese)', axis=1)


#create plots

entity_count = df['Entity owner (English)'].value_counts()
region_count = df['Region of Focus'].value_counts()

df['Total Prescence'] = df['X (Twitter) Follower #'] + df['Facebook Follower #'] + df['Instagram Follower #'] + df['Threads Follower #'] + df['YouTube Subscriber #'] + df['TikTok Subscriber #']

entity_owner = {}
for entity in df['Entity owner (English)'].unique():
    parent = df['Parent entity (English)'].where(df['Entity owner (English)'] == entity).dropna().values[0]
    entity_owner[entity] = parent

res = dict(sorted(Counter(entity_owner.values()).items(), key=lambda item: item[1]))


Y1 =entity_count

X2 = res.keys()
Y2 = res.values()

Y3 = region_count

X4 = df['Name (English)']
Y4 = df['Total Prescence']

figure, axis = plt.subplots(2, 2)


axis[0, 0].bar(Y1.keys(),Y1)
axis[0, 0].set_title("Entity Owner Count") 
axis[0, 0].set_xticklabels([]) 
axis[0,0].set_yscale('log')

axis[0, 1].bar(X2,Y2)
axis[0, 1].set_title("Parent Entity Count") 
axis[0, 1].set_xticklabels([]) 

axis[1,0].bar(Y3.keys(),Y3)
axis[1,0].set_title("Region of Focus Count") 
axis[1,0].set_xticklabels([]) 
axis[1,0].set_yscale('log')

axis[1,1].bar(X4,Y4)
axis[1,1].set_title("Total Prescence Count") 
axis[1,1].set_xticklabels([]) 
axis[1,1].set_yscale('log')
plt.show()


