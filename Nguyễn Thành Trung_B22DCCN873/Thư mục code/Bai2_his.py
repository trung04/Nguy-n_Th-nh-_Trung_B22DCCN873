import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("result.csv", header=[0, 1])  

import os
if not os.path.exists("histograms"):
    os.makedirs("histograms")

# Vẽ histogram cho toàn giải
for col in df.columns:
    if pd.api.types.is_numeric_dtype(df[col]):  # Kiểm tra nếu cột là kiểu số
        plt.figure(figsize=(10, 6))
        sns.histplot(df[col], bins=20, kde=True)
        plt.title(f'Histogram of {col[1]} for All Players')
        plt.xlabel(col[1])
        plt.ylabel('Frequency')
        plt.grid(True)
        plt.show()

# Vẽ histogram cho từng đội
teams = df[('Team', 'Team Name')].unique()  # Lấy danh sách các đội
for team in teams:
    team_data = df[df[('Team', 'Team Name')] == team]  # Lọc dữ liệu của đội
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):  # Kiểm tra nếu cột là kiểu số
            plt.figure(figsize=(10, 6))
            sns.histplot(team_data[col], bins=20, kde=True)
            plt.title(f'Histogram of {col[1]} for {team}')
            plt.xlabel(col[1])
            plt.ylabel('Frequency')
            plt.grid(True)
            plt.show()
