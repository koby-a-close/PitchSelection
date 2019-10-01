# PitchSelection_Catchers.py
# Created: 09/26/2019

# import warnings filter
from warnings import simplefilter
# ignore all future warnings
simplefilter(action='ignore', category=FutureWarning)

# Load packages
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Import Data
data_dir = '/Users/Koby/PycharmProjects/PitchSelectionAnalysis/Input/'
df_data = pd.read_csv(data_dir + 'Syndergaard_PitchSelection_noCatchers.csv')
df_data_catchers = pd.read_csv(data_dir + 'Syndergaard_PitchSelection.csv')
df_player_names = pd.read_csv(data_dir + 'player_names.csv')

# Create a dictionary of player names to match with ID numbers
player_names = dict(zip(df_player_names.mlb_id, df_player_names.mlb_name))
# player_names = df_player_names.set_index('mlb_id').to_dict()
    # {467092: 'Wilson Ramos', 621512: 'Tomas Nido', 425784: 'Rene Rivera', 518595: 'Travis dArnaud'}

# Combine balls and strikes into a count column
df_data['count'] = df_data['balls'].astype(str)+'-'+df_data['strikes'].astype(str)
df_data_catchers['count'] = df_data_catchers['balls'].astype(str)+'-'+df_data_catchers['strikes'].astype(str)

# Divide by Batter Stance: R and L
df_Ldata = df_data[(df_data.stand == 'L')]
df_Rdata = df_data[(df_data.stand == 'R')]

# Pivot tables for Left and Right data
L_map = df_Ldata[['pitch_name', 'count', 'percentThrown']].copy()
L_map = L_map.pivot(index='pitch_name', columns='count', values='percentThrown')

R_map = df_Rdata[['pitch_name', 'count', 'percentThrown']].copy()
R_map = R_map.pivot(index='pitch_name', columns='count', values='percentThrown')

#Plot heatmaps on subplots
font = {'family': 'sans-serif',
        'color':  'black',
        'weight': 'normal',
        'size': 10,
        }

fig = plt.figure(1)
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)
ax1.set_title('Pitch Selection Breakdown by Batter Stance (Left on Top, Right on Bottom)\n All Catchers',
              fontdict=font)

sns.heatmap(L_map, vmin=0, vmax=100, annot=True, square=False, linewidths=0.2, cmap='coolwarm', fmt='.0f', ax=ax1)
ax1.set_ylim(0, len(L_map)+0.5)
sns.heatmap(R_map, vmin=0, vmax=100, annot=True, square=False, linewidths=0.2, cmap='coolwarm', fmt='.0f', ax=ax2)
ax2.set_ylim(0, len(R_map)+0.5)
plt.subplots_adjust(left=0.25, right=0.98, hspace=0.3)
# plt.tight_layout()
plt.savefig('heatmap_Syndergaard_AllCatchers.pdf')

# Break the data up by catcher
catcherIDs = list(set(df_data_catchers.catcherID))
d = {catcherID: df_data_catchers[(df_data_catchers.catcherID == catcherID)] for catcherID in catcherIDs}
L_map = df_Ldata[['pitch_name', 'count', 'percentThrown']].copy()

i = 1
for catcherID, df in d.items():
    i += 1
    name = player_names[catcherID]
    print(name)
    df_L_temp = df[(df.stand == 'L')]
    df_R_temp = df[(df.stand == 'R')]

    L_map_temp = df_L_temp[['pitch_name', 'count', 'percentThrown']].copy()
    L_map_temp = L_map_temp.pivot(index='pitch_name', columns='count', values='percentThrown')

    R_map_temp = df_R_temp[['pitch_name', 'count', 'percentThrown']].copy()
    R_map_temp = R_map_temp.pivot(index='pitch_name', columns='count', values='percentThrown')

    fig = plt.figure(i)
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    ax1.set_title\
        ('Pitch Selection Breakdown by Batter Stance (Left on Top, Right on Bottom)\nCatcher: {0}'.format(name),
         fontdict=font)

    sns.heatmap(L_map_temp, vmin=0, vmax=100, annot=True, square=False, linewidths=0.2, cmap='coolwarm', fmt='.1f', ax=ax1)
    ax1.set_ylim(0, len(L_map_temp) + 0.5)
    sns.heatmap(R_map_temp, vmin=0, vmax=100, annot=True, square=False, linewidths=0.2, cmap='coolwarm', fmt='.1f', ax=ax2)
    ax2.set_ylim(0, len(R_map_temp) + 0.5)
    plt.subplots_adjust(left=0.25, right=0.98, hspace=0.3)
    # plt.tight_layout()
    file = 'heatmap_Syndergaard_'+name+'.pdf'
    plt.savefig(file)
