import matplotlib.pyplot as plt
import pandas as pd
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

df.set_index('Name (English)', inplace=True)

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

X2 = list(res.keys())
Y2 = list(res.values())

Y3 = region_count

X4 = df['Total Prescence'].index.tolist()
Y4 = df['Total Prescence']

Y5 = df['Impact Metric']

Y6 = df['Impact Metric'] - df['Total Prescence']


plt.bar(Y1.keys(),Y1)
plt.title("No. of Accounts of each Entity Owners") 
plt.yscale('log')
plt.ylabel('log no. of accounts')
plt.xlabel('entity owners')
plt.gca().get_xaxis().set_visible(False)
#plt.show()

plt.bar(X2,Y2)
plt.title("No. of Entity Owners of each Parent") 
plt.xlabel('parent entity')
plt.ylabel('no. of entity owners')
plt.gca().get_xaxis().set_visible(False)
#plt.show()

plt.bar(Y3.keys(),Y3)
plt.title("Region of Focus Account Number") 
plt.xlabel('no. region of focus')
plt.ylabel('log no. of accounts')
plt.gca().get_xaxis().set_visible(False)
plt.yscale('log')
#plt.show()

plt.bar(X4,Y4)
plt.title("Total Following") 
plt.gca().get_xaxis().set_visible(False)
plt.xlabel('account')
plt.ylabel('log total following')
plt.yscale('log')
#plt.show()

plt.bar(X4,Y5)
plt.title("Impact Rating") 
plt.xlabel('account')
plt.ylabel('log impact rating')
plt.gca().get_xaxis().set_visible(False)
plt.yscale('log')
#plt.show()

plt.bar(X4,Y6)
plt.title("Difference Between Metric and Total") 
plt.xlabel('account')
plt.ylabel('difference')
plt.gca().get_xaxis().set_visible(False)
#plt.show()

def write_report(Y):
    print(f'The mean of this set is {np.mean(Y)}')
    print(f'The quartiles are: Q1 = {np.quantile(Y,0.25)}, Q2 = {np.quantile(Y,0.5)}, Q3 = {np.quantile(Y,0.75)}')


series = [Y1,Y2,Y3,Y4,Y5,Y6]
for i in range(6):
    if i == 0:
        write_report(series[i])
        print(f'The top entity owners are {series[i].head(10)}')
    if i == 1:
        write_report(series[i])
        print(f'The top parent entities are {X2[0:10]}')
    if i == 2:
        write_report(series[i])
        print(f'The top regions of focus are {series[i].head(10)}')
    elif i == 3 or i == 4:
        write_report(series[i])
        print(f'The top accounts are {series[i].head(10)}')


