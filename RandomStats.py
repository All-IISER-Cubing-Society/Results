#%%
import pandas as pd

from Results import load_data, load_event_data
# %%
data = load_data()

# %%

# People who participated in the most events
print("People who participated in most events")
data['Name'].value_counts()

# %%

# People who participated in the most 3x3 events
print("People who participated in most 3x3 events")
data[data['Event'] == '3x3']['Name'].value_counts()
# %%

# People who participated in the most weekly races
print("People who participated in the most weekly races")
ne_df = data.groupby(['Name', 'Event']).count()

ne_df.reset_index(inplace=True)

max_dates = {participant: ne_df[ne_df['Name'] == participant]['Date'].max() for participant in ne_df['Name'].unique()}

dict(sorted(max_dates.items(), key=lambda item: item[1], reverse=True))
# %%

# Finding closest calls
print("Closest Calls")
nodnf_data = data[data['Result'] != 'DNF']
nodnf_data['Result'] = nodnf_data['Result'].astype(float)
nodnf_data.reset_index(inplace=True)
nodnf_data.drop(columns=['index'])

closest_calls = nodnf_data['Result'].diff().abs().sort_values()

closest_calls_locs = list(closest_calls.index)[0:4]

for loc in closest_calls_locs:
    print(nodnf_data.iloc[loc-1:loc+1])
    print()

# %%

# Longest Participation Streak
print("Longest Participation Streak")
dates = data['Date'].unique()
names = data['Name'].unique()

current_streak = {name: 0 for name in names}
max_streak = {name: 0 for name in names}
participated = {name: False for name in names}

for date in sorted(dates):
    current_data = data[data['Date'] == date]
    
    participated_people = current_data['Name'].unique()
    
    for person in participated_people:
        participated[person] = True
        current_streak[person] += 1
        max_streak[person] = max(max_streak[person], current_streak[person])
        
    for person in participated:
        if not participated[person]:
            current_streak[person] = 0

    participated = {name: False for name in names}

dict(sorted(max_streak.items(), key=lambda item: item[1], reverse=True))

    
# %%
