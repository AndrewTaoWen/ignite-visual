import pandas as pd
import numpy as np

df = pd.read_excel("data.xlsx", sheet_name=0)
data = df.to_numpy()

NUM_COLS = len(data[0])
NUM_ROWS = len(data)

map_dict = {}

for i in range(NUM_ROWS):
    
    actor = data[i][0]
    affiliates = []
    for j in range(1,NUM_COLS):
        if not pd.isna(data[i][j]):
            affiliates.append(data[i][j])
   
    map_dict[actor] = set(affiliates)
        
print(map_dict)