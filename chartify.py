import io
import pandas as pd
import requests
import time
import tqdm


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