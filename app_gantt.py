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

def header():
    return html.Header(children=[
        html.Nav(className="grey darken-3", children=[
            html.Div(className="nav-wrapper", children=[
                html.A(style={"margin-left":"1%"}, href="#", className="brand-logo", children="De olho no Metrô"),
                html.Ul(className="right hide-on-med-and-down", children=[
                    html.Li(children=html.A(href="", children="Relatório dia")),
                    html.Li(children=html.A(href="", children="Relatório mês")),
                    html.Li(children=html.A(href="", children="Sobre")),
                    html.Li(children=html.A(className="waves-effect waves-light btn", href="", children="Baixar os dados")),
                ])
            ])
        ]),
    ])

def day_report():
    return html.Div(className="row valign-wrapper", children=[
        html.Div(style={"padding":"3%"}, id="input", className="col s3", children=[
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
        html.Div(style={"padding-left":"7%"}, id='chart', className='col s9', children=[
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



app.layout = html.Main(children=[
    header(),
    day_report(),
])

# app.layout = html.Div(
#     [
#         html.Nav(className="grey darken-3", children=[
#             html.Div(className="nav-wrapper", children=[
#                 html.A(style={"margin-left":"1%"}, href="#", className="brand-logo", children="De olho no Metrô"),
#                 html.Ul(className="right hide-on-med-and-down", children=[
#                     html.Li(children=html.A(href="", children="Sobre")),
#                     html.Li(children=html.A(className="waves-effect waves-light btn", href="", children="Baixar os dados")),
#                 ])
#             ])
#         ]),
#         html.Ul(id="slide-out", className="sidenav", children=[
#             html.Li(html.A(href="#!", children="Link")),
#         ]),
#     ]
# )


# app.layout = html.Div(className="three columns", children=[
#         html.H3(className="center-align", children='Veja o histórico do transporte sobre trilhos de SP'),
#         html.Div([
#             html.H5(children='Linha'),
#             dcc.Dropdown(
#                 id='lines-dropdown',
#                 options=[{'label': i.capitalize(), 'value': i} for i in df.Line.unique()],
#                 value='azul'
#             ),
#             html.H5(children='Dia'),
#             dcc.DatePickerSingle(
#                 id='date-picker-single',
#                 min_date_allowed=df['Time'].min(),
#                 max_date_allowed=df['Time'].max(),
#                 initial_visible_month=df['Time'].max(),
#                 date=datetime(2018,7,25),
#                 display_format='DD/MM/YYYY'
#             )
#         ]),
#         html.Div(
#             id='chart',
#             className='center-align',
#             children=[
#                 dcc.Graph(
#                     id='gantt-plot',
#                     config={
#                         'displayModeBar': False,
#                         'showAxisDragHandles':False,
#                         'autosizable':True
#                     }
#                 )
#         ])
# ])

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