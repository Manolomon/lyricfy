import pandas as pd
import requests
import tqdm

features = []
track_data = []
spotify_attr = ['Track Id', 'acousticness', 'danceability', 'duration_ms', 'energy', 'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'speechiness', 'tempo', 'time_signature', 'valence']
token = "BQAc-ZEx8MyKn2s0kQDfdcsJWIDpHfpkEPqIgTPkAeFs95ecvzk3aJnV9rsYOnoT6NnRyvULXHJQ30tVecNMInv7aU7zDtHHDnBm8Pte_sIi63PkIVm7yBu32b5clzpdyr9Yxf_c8ezMno59gssqGZhwQbXhsyIXLgKezKyX3g"
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