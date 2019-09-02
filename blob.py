# To add a new cell, type '#%%'
# To add a new markdown cell, type '#%% [markdown]'

#%% [markdown]

# # Esta parte del código se obtiene de [un repositorio](https://github.com/fbkarsdorp/spotify-chart)
# Holis
#%%

import io
import pandas as pd
import json
import requests
import time
import tqdm
import numpy as np

def week_dates(date, weekday=0):
    week_start = date - pd.DateOffset(weekday=weekday, weeks=1)
    week_end = date + pd.DateOffset(weekday=weekday, weeks=0)
    return week_start, week_end


def get_chart(date, region='en', freq='daily', chart='top200'):
    chart = 'regional' if chart == 'top200' else 'viral'
    date = pd.to_datetime(date)
    if date.year < 2017:
        raise ValueError('No chart data available from before 2017')
    if freq == 'weekly':
        start, end = week_dates(date, weekday=4)
        date = f'{start.date()}--{end.date()}'
    else:
        date = f'{date.date()}'
    url = f'https://spotifycharts.com/{chart}/{region}/{freq}/{date}/download'
    data = io.StringIO(requests.get(url).text)
    try:
        df = pd.read_csv(data, skiprows=1) # Fix Spotify's Note
    except pd.errors.ParserError:
        df = None
        print(data)
    return df


def get_charts(start, end=None, region='en', freq='daily', chart='top200', sleep=1):
    sample = 'D' if freq == 'daily' else 'W'
    end_date = start if end == None else end
    dfs = []
    for date in tqdm.tqdm(pd.date_range(start=start, end=end_date, freq=sample)):
        df = get_chart(date, region=region, freq=freq, chart=chart)
        if df is not None:
            df['Date'] = date
            df = df.head(50)
            dfs.append(df)
            time.sleep(sleep)
    return pd.concat(dfs, ignore_index=True)


#%%
chart = get_charts('2019-08-01','2019-08-23', freq='daily', region='mx')


#%%
chart['Track Id'] = chart['URL'].str.split("/",expand=True)[4]


#%%

# for row in df.head(100).itertuples(): Para las llamadas
features = []
track_data = []
spotify_attr = ['Track Id', 'acousticness', 'danceability',
                'duration_ms', 'energy', 'instrumentalness',
                'key', 'liveness', 'loudness', 'mode',
                'speechiness', 'tempo', 'time_signature',
                'valence']
token = "BQDIFpQzT1bJDRJAMfzvcG0_8sjGCjBCsJ8UUxqgSfmo_BjwDBlJDs9HHJWSc6yHwsGpZi7NcQRbU5CB3HkulaH3Me7xnXT47WLSO5xXLD0AuaRAX3vTGHqbPovJU8u88I0hycO8SzbyVcQXzXHL0G-KcnvD9YCi6XH6KIMUEA"
chart_unique = chart.drop_duplicates('Track Id')
for index, row in tqdm.tqdm(chart_unique.iterrows(), total=chart_unique.shape[0]):
    JSONContent = requests.get("https://api.spotify.com/v1/audio-features/" + row['Track Id'],
    headers={
        "Accept": "application/json",
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json"
    },
    cookies={},
    ).json()
    track_data.append(row['Track Id'])
    for attr in spotify_attr[1:]:
        track_data.append(JSONContent[attr])
    features.append(track_data)
    #print(track_data)
    track_data = []
    dataset = pd.DataFrame(features)


#%%
dataset.columns = spotify_attr


#%%
test = pd.merge(chart, dataset, on='Track Id', how='left', left_index=True)


#%%
test


#%%



