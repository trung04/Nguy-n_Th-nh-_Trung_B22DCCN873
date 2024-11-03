import pandas as pd
import numpy as np
df = pd.read_csv("result.csv", header=[0, 1]) 
total_scores=df.select_dtypes(include='number')
total_scores[('Info','Team')] = df[('Info','Team')]
total_scores=total_scores.groupby(('Info','Team')).mean()
best_teams = {}
# Duyệt qua từng cột của DataFrame để tìm đội bóng có điểm cao nhất
for col in df.columns:
    if pd.api.types.is_numeric_dtype(df[col]):
    #     # Tìm đội bóng có tổng điểm cao nhất
        best_team = total_scores[col].idxmax()
        max_score = total_scores[col].max()
        print(f" - Đội bóng có chỉ số: {col} cao nhất: {best_team} với tổng điểm: {max_score}")

