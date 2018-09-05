import pandas as pd

def import_data(path):
    '''
    Import data from csv file and make initial preparation
    '''
    df = pd.read_csv(path)
    df['Time'] = pd.to_datetime(df['Time'], format="%Y-%m-%d %H:%M")


def gantt_filter(df):
    '''
    Returns dataFrame plottable using plotly's Gantt chart
    '''
    gantt_df = pd.DataFrame()
    df = df.loc[df['Status'].shift() != df['Status']]
    gantt_df['Task'] = df['Status']
    gantt_df['Start'] = df['Time']
    gantt_df['Finish'] = df['Time'].shift(-1)
    gantt_df = gantt_df[
        (gantt_df['Finish'] - gantt_df['Start']).dt.days < 1
        ]
    return gantt_df

def time_filter(df, day, month, year):
    '''
    Selects single day of data from gantt-ready dataframe
    '''
    filtered = df[
        (df['Start'].dt.month == month) &
        (df['Start'].dt.day == day) &
        (df['Start'].dt.year == year)
    ]
    filtered.reset_index(drop=True, inplace=True)
    return filtered
