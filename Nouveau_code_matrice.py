# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 14:05:24 2024

@author: Zbida
"""
import pandas as pd
from collections import defaultdict

# Step 1: Read the 'cast' sheet from the Excel file into a pandas DataFrame
df = pd.read_excel(r'netflix_titles.xlsx', sheet_name='liste_des_noms_acteurs')
dd = pd.read_excel(r'netflix_titles.xlsx', sheet_name='Acteurs_Unique')

df_list = df.values.tolist()
dd_list = dd.values.tolist()

# Create a dictionary where keys are films and values are actors in that film
film_actor_dict = defaultdict(set)
for film_idx, film_cast in enumerate(df_list):
    for actor in film_cast:
        film_actor_dict[tuple(film_cast)].add(actor)  # Convert list to tuple

n = len(dd_list)

# Create a matrix filled with zeros of size n x n
Mat = [[0] * n for _ in range(n)]

# Iterate over all pairs of actors
for i in range(n):
    for j in range(i, n):
        if i == j:
            Mat[i][j] = 1  # Consider actor is related to themselves
        else:
            for film_cast, film_actors in film_actor_dict.items():
                if dd_list[i] in film_actors and dd_list[j] in film_actors:
                    Mat[i][j] = 1
                    Mat[j][i] = 1  # Ensure matrix symmetry
                    break

# Writing the matrix to the Excel file
with pd.ExcelWriter('netflix_titles.xlsx', engine='openpyxl', mode='a') as writer:
    pd.DataFrame(Mat).to_excel(writer, sheet_name='please_work', index=False)
