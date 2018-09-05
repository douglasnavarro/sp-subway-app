import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.figure_factory as ff

df = pd.read_csv('subway-data-clean.csv')
df['Time'] = pd.to_datetime(df['Time'], format="%Y-%m-%d %H:%M")

df = df[df['Line'] == 'azul']

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

def drop_weird(df):
    df = df[(df['Finish'] - df['Start']).dt.days < 1]
    return df

def time_filter(df, day, month, year):
    '''
    Selects single day of data from gantt-ready dataframe
    '''
    return df[
        (df['Start'].dt.month == month) &
        (df['Start'].dt.day == day) &
        (df['Start'].dt.year == year)
    ]

#df_plot = time_filter(df, 25, 7, 2018)
plottable = gantt_filter(df)
#df_plot = drop_weird(df_plot)
plottable = time_filter(plottable, 25, 7, 2018)
plottable.reset_index(drop=True, inplace=True)
plottable.to_csv('test.csv')

fig = ff.create_gantt(plottable, group_tasks=True, title='Operação', bar_width=0.3, showgrid_x=True, showgrid_y=True)

app = dash.Dash(__name__)
server = app.server


'''
~~~~~~~~~~~~~~~~
~~ APP LAYOUT ~~
~~~~~~~~~~~~~~~~
'''

app.layout = html.Div(className="container", children=[
        html.H3(className="center-align", children='Veja o histórico do transporte sobre trilhos de SP'),
        html.Div([
            html.H5(children='Linha'),
            dcc.Dropdown(
                id='lines-dropdown',
                options=[{'label': i, 'value': i} for i in df.Line.unique()]
            ),
            html.H5(children='Dia'),
            dcc.DatePickerSingle(
                id='date-picker-single',
                min_date_allowed=df['Time'].min(),
                max_date_allowed=df['Time'].max(),
                initial_visible_month=df['Time'].max(),
                date=df['Time'].max()
            )
        ]),
        html.Div(className='center-align',children=[
            dcc.Graph(figure=fig, id='gantt')
        ])
])


if __name__ == '__main__':
    app.run_server()