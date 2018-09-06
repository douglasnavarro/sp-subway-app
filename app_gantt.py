import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objs as go
from prepare_data import gantt_filter, time_filter
from datetime import datetime

df = pd.read_csv('subway-data-clean.csv')
df['Time'] = pd.to_datetime(df['Time'], format="%Y-%m-%d %H:%M")

app = dash.Dash(__name__)
server = app.server

'''
The layout of the app is a big title,
an input component for the line
an input component for the date
and of course a chart
'''
app.layout = html.Div(className="container", children=[
        html.H3(className="center-align", children='Veja o histórico do transporte sobre trilhos de SP'),
        html.Div([
            html.H5(children='Linha'),
            dcc.Dropdown(
                id='lines-dropdown',
                options=[{'label': i.capitalize(), 'value': i} for i in df.Line.unique()],
                value='azul'
            ),
            html.H5(children='Dia'),
            dcc.DatePickerSingle(
                id='date-picker-single',
                min_date_allowed=df['Time'].min(),
                max_date_allowed=df['Time'].max(),
                initial_visible_month=df['Time'].max(),
                date=datetime(2018,7,25),
                display_format='DD/MM/YYYY'
            )
        ]),
        html.Div(
            id='chart',
            className='center-align',
            children=[
                dcc.Graph(
                    id='gantt-plot',
                    config={
                        'displayModeBar': False,
                        'showAxisDragHandles':False,
                        'autosizable':True
                    }
                )
        ])
])

'''
The app needs to be able to
update the chart using the
variables input by the user
'''
@app.callback(
    dash.dependencies.Output('gantt-plot', 'figure'),
    [dash.dependencies.Input('date-picker-single', 'date'),
     dash.dependencies.Input('lines-dropdown', 'value')
    ])
def update_gantt(date, value):
    converted_date = datetime.strptime(date, '%Y-%m-%d')
    line_filtered = df[df['Line'] == value]
    filtered_df = gantt_filter(line_filtered)
    filtered_df = time_filter(filtered_df, converted_date.day,converted_date.month,converted_date.year)
    filtered_df.reset_index(drop=True, inplace=True)
    if filtered_df.empty:
        title = 'Não há dados para a data e linha selecionadas.'
    else:
        title = 'Operação da linha {} na data {}'.format(value.capitalize(), converted_date.strftime('%d/%m/%Y'))
    fig = ff.create_gantt(
        filtered_df,
        group_tasks=True,
        title=title,
        bar_width=0.3,
        showgrid_x=True,
        showgrid_y=False
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)