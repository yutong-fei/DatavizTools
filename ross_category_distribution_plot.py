import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from collections import OrderedDict

path = "XXX.csv"
df = pd.read_csv(path)
df.head()

df_count = df.groupby(['argument categories', 'open science taxonomy']).size().reset_index(name='count')
df_pivot = df_count.pivot(index='argument categories', columns='open science taxonomy', values='count').fillna(0)
df_percent = df_pivot.div(df_pivot.sum(axis=1), axis=0) * 100


fig, ax = plt.subplots(figsize=(12, 10))
df_pivot.plot(kind='bar', stacked=True, ax=ax, colormap='tab20')

ax.set_xlim(-0.5, len(df_pivot) - 0.2)
threshold = 1


for i, (idx, row) in enumerate(df_pivot.iterrows()):
    cumulative = 0  
    
    for aspect in df_pivot.columns:
        count = row[aspect] 
        
        if count > 0:
            percent = df_percent.loc[idx, aspect]  
            
            if percent >= threshold:
                y = cumulative + count / 2
                x = i + 0.25  
                ax.text(x, y, f"{percent:.1f}%", ha='left', va='center', fontsize=7, color='black')
            
            # Tracer une ligne blanche entre les segments empilés
            if cumulative > 0:
                ax.plot([i - 0.4, i + 0.4], [cumulative, cumulative], color='white', linewidth=0.8)
            
            cumulative += count  

    total_count = int(row.sum())
    ax.text(i, cumulative + 0.05, f"{total_count}", ha='center', va='bottom', fontsize=10, color='black', fontweight='bold')

ax.set_title("Distribution of Open Science Taxonomy across Identified Categories of Critical Arguments", fontsize=16)
ax.set_xlabel("Argument Categories", fontsize=14)
ax.set_ylabel("Count", fontsize=14)
plt.xticks(rotation=45, ha="right", fontsize=10)
plt.yticks(fontsize=10)

plt.legend(title='Open Science Taxonomy', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=12)
plt.tight_layout()
plt.show()
