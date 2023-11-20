import matplotlib.pyplot as plt
import pandas as pd
import pyvis as pv
import numpy as np
from collections import Counter

#import data


data_file = "data.xlsx"
df = pd.read_excel(data_file)



#clean some data
df = df.drop('Name (Chinese)', axis=1)
df = df.drop('Entity owner (Chinese)', axis=1)
df = df.drop('Parent entity (Chinese)', axis=1)

df['X (Twitter) Follower #']=df['X (Twitter) Follower #'].fillna(0)
df['Facebook Follower #']=df['Facebook Follower #'].fillna(0)
df['Instagram Follower #'] = df['Instagram Follower #'] .fillna(0)
df['Threads Follower #'] = df['Threads Follower #'].fillna(0)
df['YouTube Subscriber #']  = df['YouTube Subscriber #'] .fillna(0)
df['TikTok Subscriber #'] = df['TikTok Subscriber #'].fillna(0)

#total following for each account
df['Total Prescence'] = df['X (Twitter) Follower #'] + df['Facebook Follower #'] + df['Instagram Follower #'] + df['Threads Follower #'] + df['YouTube Subscriber #'] + df['TikTok Subscriber #']

df = df[df['Total Prescence'] != 0]

#add an impact metric that accounts for diversity of social media prescence

numeric = df[['Total Prescence', 'X (Twitter) Follower #', 'Facebook Follower #', 'Instagram Follower #', 'Threads Follower #',
                         'YouTube Subscriber #', 'TikTok Subscriber #']]



def scale(row):
    return row['Total Prescence']/(np.std([row['X (Twitter) Follower #']/row['Total Prescence'], row['Facebook Follower #']/row['Total Prescence'],
                                                     row['Instagram Follower #']/row['Total Prescence'], row['Threads Follower #']/row['Total Prescence'], 
                                                     row['YouTube Subscriber #']/row['Total Prescence'], row['TikTok Subscriber #']/row['Total Prescence']])/np.std([1,0,0,0,0,0]))

df['Impact Metric'] = numeric.apply(scale, axis=1)


#create plots

#unique entity owners
entity_count = df['Entity owner (English)'].value_counts()

#unique regions
region_count = df['Region of Focus'].value_counts()


#map each parent entity to number of entity owners it owns
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

Y5 = df['Impact Metric']

Y6 = df['Impact Metric'] - df['Total Prescence']

print(Y6)

figure, axis = plt.subplots(2, 3)


axis[0, 0].bar(Y1.keys(),Y1)
axis[0, 0].set_title("Entity Owner Count") 
axis[0,0].set_yscale('log')
axis[0,0].get_xaxis().set_visible(False)

axis[0, 1].bar(X2,Y2)
axis[0, 1].set_title("Parent Entity Count") 
axis[0, 1].get_xaxis().set_visible(False)

axis[0,2].bar(Y3.keys(),Y3)
axis[0,2].set_title("Region of Focus Count") 
axis[0,2].get_xaxis().set_visible(False)
axis[0,2].set_yscale('log')

axis[1,0].bar(X4,Y4)
axis[1,0].set_title("Total Prescence Count") 
axis[1,0].get_xaxis().set_visible(False)
axis[1,0].set_yscale('log')

axis[1,1].bar(X4,Y5)
axis[1,1].set_title("Impact Metric") 
axis[1,1].get_xaxis().set_visible(False)
axis[1,1].set_yscale('log')

axis[1,2].bar(X4,Y6)
axis[1,2].set_title("Difference Between Metric and Total") 
axis[1,2].get_xaxis().set_visible(False)
plt.show()


