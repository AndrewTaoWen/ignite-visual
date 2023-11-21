import pandas as pd
import numpy as np
import json  # Import the json module

# Read the Excel file
df = pd.read_excel("data.xlsx", sheet_name=0)

arr = df["Region of Focus"]

# Convert DataFrame to NumPy array (if needed)
data = df.to_numpy()

NUM_COLS = len(data[0])
NUM_ROWS = len(data)

# Get column names
column_names = df.columns.tolist()

heiarchy_tree = {"Ministry of Foreign Affairs":[]}

json_dict = dict()

for i in range(NUM_ROWS):

    name = data[i][0]
    d = dict()

    for j in range(1,NUM_COLS):

        value = data[i][j]
        
        if not pd.isna(value):
            d[column_names[j]] = data[i][j]
        else:
            d[column_names[j]] = "None"

    json_dict[name] = d


with open("output.json", "w") as json_file:
    json.dump(json_dict, json_file, indent=4)


