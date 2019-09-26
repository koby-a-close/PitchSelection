# HeatMapGenerator-v1.py
# Created: 09/26/2019

# import warnings filter
from warnings import simplefilter
# ignore all future warnings
simplefilter(action='ignore', category=FutureWarning)

# Load packages
import numpy as np
import pandas as pd
from xgboost import XGBRegressor
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
import seaborn as sns

# Import Data
data_dir = '/Users/Koby/PycharmProjects/PitchSelectionAnalysis/Input/'
df_data = pd.read_csv(data_dir + 'Syndergaard_PitchSelection_noCatchers.csv')
df_data_catchers = pd.read_csv(data_dir + 'Syndergaard_PitchSelection.csv')

# Divide by Batter Stance: R and L
L_data = df_data[(df_data.stand == 'L')]
L_data['count'] = L_data['balls'].astype(str)+'-'+L_data['strikes'].astype(str)
R_data = df_data[(df_data.stand == 'R')]
R_data['count'] = R_data['balls'].astype(str)+'-'+R_data['strikes'].astype(str)

# Heatmap for Left and Right in a single window
L_map = L_data[['pitch_name', 'count', 'percentThrown']].copy()
L_map = L_map.pivot(index='pitch_name', columns='count', values='percentThrown')

R_map = R_data[['pitch_name', 'count', 'percentThrown']].copy()
R_map = R_map.pivot(index='pitch_name', columns='count', values='percentThrown')

fig = plt.figure(1)
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)
ax1.title.set_text('Pitch Selection Breakdown by Batter Stace (Left on Top, Right on Bottom)')

sns.heatmap(L_map, vmin=0, vmax=100, annot=True, square=False, linewidths=0.2, cmap='coolwarm', ax=ax1)
ax1.set_ylim(0, len(L_map)+0.5)
sns.heatmap(R_map, vmin=0, vmax=100, annot=True, square=False, linewidths=0.2, cmap='coolwarm', ax=ax2)
ax2.set_ylim(0, len(R_map)+0.5)
plt.show()

#TODO: Need to figure out how to break up data by catcherID, then redo analysis with that subgrouping
