# PitchSelection_PrevPitch.py
# Created: 09/28/2019

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

# Font preferences
font = {'family': 'sans-serif',
        'color':  'black',
        'weight': 'normal',
        'size': 10,
        }

# Import Data
data_dir = '/Users/Koby/PycharmProjects/PitchSelectionAnalysis/Input/'
df_data = pd.read_csv(data_dir + 'Syndergaard_rawdata.csv')
df_player_names = pd.read_csv(data_dir + 'player_names.csv')

# Create a dictionary of player names to match with ID numbers
player_names = dict(zip(df_player_names.mlb_id, df_player_names.mlb_name))

# Get relevant rows from the raw data and get a count column using balls and strikes
df_data['count'] = df_data['balls'].astype(str)+'-'+df_data['strikes'].astype(str)
df_pitch_data = df_data[['fielder_2', 'stand', 'count', 'pitch_name', 'type']].copy()
df_pitch_data.rename(columns={'fielder_2':'catcherID'}, inplace=True)

df_temp = df_data[['count', 'pitch_name', 'type']].copy()
df_temp.rename(columns={'count':'prev_count','pitch_name':'prev_pitch_name','type':'prev_type'}, inplace=True)
frames = [df_pitch_data, df_temp]

df_pitch_data = pd.concat(frames, axis=1)
df_pitch_data['prev_count'] = df_pitch_data['prev_count'].shift(-1)
df_pitch_data['prev_pitch_name'] = df_pitch_data['prev_pitch_name'].shift(-1)
df_pitch_data['prev_type'] = df_pitch_data['prev_type'].shift(-1)

# get all possible counts in a sorted list, remove NaNs
counts = list(set(df_pitch_data['count']))
counts = [x for x in counts if str(x) != 'nan']
counts = sorted(counts)
counts.pop(0)

# get all catcher IDs in a sorted list, remove Nans
catcherIDs = list(set(df_pitch_data.catcherID))
catcherIDs = [x for x in catcherIDs if str(x) != 'nan']
catcherIDs = sorted(catcherIDs)


figure_number = 0
for cnt in counts:
    df_count = df_pitch_data[(df_pitch_data['count'] == cnt)]
    df_count['prev_pitch'] = df_count['prev_pitch_name'].astype(str) + ', ' + df_count['prev_type'].astype(str)
    d = {catcherID: df_count[(df_count.catcherID == catcherID)] for catcherID in catcherIDs}

    pitches = list(set(df_count.pitch_name))
    pitches = [x for x in pitches if str(x) != 'nan']
    pitches = sorted(pitches)
    df_pitches = pd.DataFrame({'pitches': pitches})

    for catcherID, df in d.items():
        name = player_names[catcherID]
        print(name)
        df_L = df[(df.stand == 'L')]
        df_L = df_L[['prev_pitch', 'pitch_name']].copy()
        df_L_ratios = pd.DataFrame({'prev_pitches': list(set(df_L.prev_pitch))})
        df_L_ratios = df_L_ratios.sort_values(by=['prev_pitches'])

        df_R = df[(df.stand == 'R')]
        df_R = df_R[['prev_pitch', 'pitch_name']].copy()
        df_R_ratios = pd.DataFrame({'prev_pitches': list(set(df_R.prev_pitch))})
        df_R_ratios = df_R_ratios.sort_values(by=['prev_pitches'])
        i = 0
        k = 0
        for pitch in df_pitches.pitches:
            i += 1
            k += 1
            j = -1
            l = -1
            df_L_ratios['{0}'.format(pitch)] = ''
            df_R_ratios['{0}'.format(pitch)] = ''
            for p_pitch in df_L_ratios.prev_pitches:
                j += 1
                t = len(df_L[(df_L['prev_pitch'] == p_pitch) & (df_L['pitch_name'] == pitch)])
                n = len(df_L[(df_L['prev_pitch'] == p_pitch)])
                if n > 0:
                    usage = round(t / n * 100, 2)
                if n == 0:
                    usage = 0
                df_L_ratios.iloc[j, i] = usage
            for p_pitch in df_R_ratios.prev_pitches:
                l += 1
                times_thrown = len(df_R[(df_R['prev_pitch'] == p_pitch) & (df_R['pitch_name'] == pitch)])
                number_occurances = len(df_R[(df_R['prev_pitch'] == p_pitch)])
                if number_occurances > 0:
                    usage = round(times_thrown / number_occurances * 100, 2)
                if number_occurances == 0:
                    usage = 0
                df_R_ratios.iloc[l, k] = usage

        df_L_ratios = df_L_ratios.set_index('prev_pitches')
        df_L_ratios = df_L_ratios.astype(float)
        df_R_ratios = df_R_ratios.set_index('prev_pitches')
        df_R_ratios = df_R_ratios.astype(float)

        figure_number += 1
        fig = plt.figure(figure_number)
        ax1 = fig.add_subplot(211)
        ax2 = fig.add_subplot(212)
        ax1.set_title \
            ('Pitch Breakdown by Batter Stance (Left on Top, Right on Bottom)\nCatcher: {0}, Count: {1}'.format(name, cnt),
             fontdict=font)

        sns.heatmap(df_L_ratios, vmin=0, vmax=100, annot=True, square=False, linewidths=0.2, cmap='coolwarm', fmt='.1f',
                    ax=ax1)
        ax1.set_ylim(0, len(df_L_ratios) + 0.5)
        sns.heatmap(df_R_ratios, vmin=0, vmax=100, annot=True, square=False, linewidths=0.2, cmap='coolwarm', fmt='.1f',
                    ax=ax2)
        ax2.set_ylim(0, len(df_R_ratios) + 0.5)
        plt.subplots_adjust(left=0.25, right=0.98, hspace=0.3)
        # plt.tight_layout()
        file = 'PitchSelection_Syndergaard_' + name + '_' + cnt + '.pdf'
        plt.savefig(file)

