import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

data = pd.read_excel(r"./data.xlsx")

# Set the aesthetic style of the plots
sns.set(style="whitegrid")

# Data Preparation for Visualizations
# 1. Platform-Wise Reach
platforms = ['X (Twitter) Follower #', 'Facebook Follower #', 'Instagram Follower #', 
             'YouTube Subscriber #', 'TikTok Subscriber #']
platform_reach = data[platforms].sum()

# 2. Language Distribution
language_distribution = data['Language'].value_counts()

# 3. Region of Focus Distribution
region_distribution = data['Region of Focus'].value_counts()

# Creating the Visualizations
plt.figure(figsize=(18, 6))

# Platform-Wise Reach Bar Graph
plt.subplot(1, 3, 1)
sns.barplot(x=platform_reach.index, y=platform_reach.values, palette="viridis")
plt.title('Social Media Reach by Platform')
plt.xticks(rotation=45)
plt.ylabel('Total Followers/Subscribers')
plt.xlabel('Platform')

# Language Distribution Pie Chart
plt.subplot(1, 3, 2)
language_distribution.plot(kind='pie', autopct='%1.1f%%', startangle=140, cmap='Set3')
plt.title('Language Distribution')
plt.ylabel('')

# Region of Focus Distribution Bar Graph
plt.subplot(1, 3, 3)
sns.barplot(x=region_distribution.index, y=region_distribution.values, palette="mako")
plt.title('Region of Focus Distribution')
plt.xticks(rotation=45)
plt.ylabel('Number of Entities')
plt.xlabel('Region of Focus')

# Adjust layout to prevent overlap
plt.tight_layout()

# Show the plots
plt.show()
