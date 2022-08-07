from datetime import datetime as dt
# import dash_auth
# login in option
import dash
import dash_bootstrap_components as dbc
from dash import dash_table
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from entry_data import *

df, fig, fig1, fig2, fig3, fig4 = data_load()

# login in option
# # Keep this out of source code repository - save in a file or a database
# VALID_USERNAME_PASSWORD_PAIRS = {
#     'admin': 'admin'
# }

# themes bootstrap template LUX
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])
# login in option
# auth = dash_auth.BasicAuth(
#     app,
#     VALID_USERNAME_PASSWORD_PAIRS
# )

# setting a source data of dropdown lists, sorted
branches = df['user name'].sort_values(ascending=True).unique().tolist()
branches1 = df['Project name'].sort_values(ascending=True).unique().tolist()
branches2 = df['Customer Name'].sort_values(ascending=True).unique().tolist()

# dash app, components
app.layout = html.Div([
    # data picker range, set to display monthly date
    dbc.Row([
        dbc.Col([html.H5(className='text-center'),
                 dcc.DatePickerRange(
                     id='my-date-picker-range',  # ID to be used for callback
                     calendar_orientation='horizontal',  # vertical or horizontal
                     day_size=39,  # size of calendar image. Default is 39
                     end_date_placeholder_text="Return",  # text that appears when no end date chosen
                     with_portal=False,  # if True calendar will open in a full screen overlay portal
                     first_day_of_week=0,  # Display of calendar when open (0 = Sunday)
                     reopen_calendar_on_clear=True,
                     is_RTL=False,  # True or False for direction of calendar
                     clearable=False,  # whether the user can clear the dropdown
                     number_of_months_shown=1,  # number of months shown when calendar is open
                     min_date_allowed=dt(2018, 1, 1),  # minimum date allowed on the DatePickerRange component
                     max_date_allowed=dt.today(),  # maximum date allowed on the DatePickerRange component
                     initial_visible_month=dt.today(),  # the month initially presented when the user opens the calendar
                     # end_date_placeholder_text='DD-MM-YYYY',
                     start_date=dt(2020, 1, 1).date(),
                     end_date=dt.today().date(),
                     display_format='MM YYYY',  # how selected dates are displayed in the DatePickerRange component.
                     month_format='MMMM, YYYY',  # how calendar headers are displayed when the calendar is opened.
                     minimum_nights=0,  # minimum number of days between start and end date
                     persistence=True,
                     persisted_props=['start_date'],
                     persistence_type='session',  # session, local, or memory. Default is 'local'
                     updatemode='singledate'  # singledate or bothdates. Determines when callback is triggered
                 )], width={'size': 2, "offset": 0, 'order': 1}),

        # dropdown customers
        dbc.Col([html.H5(className='text-center'),
                 dcc.Dropdown(
                     id='customer_dropdown', placeholder="Customer",
                     options=[{'label': br, 'value': br} for br in branches2],
                     value=[],
                     multi=True,
                     disabled=False,
                     clearable=True,
                     searchable=True)], width={'size': 2, "offset": 0, 'order': 1}),

        # dropdown projects
        dbc.Col([html.H5(className='text-center'),
                 dcc.Dropdown(
                     id='project_dropdown', placeholder="Project",
                     options=[{'label': br, 'value': br} for br in branches1],
                     value=[],
                     multi=True,
                     disabled=False,
                     clearable=True,
                     searchable=True)], width={'size': 3, "offset": 0, 'order': 1}),

        # dropdown user
        dbc.Col([html.H5(className='text-center'),
                 dcc.Dropdown(
                     id='filter_dropdown', placeholder="User Name",
                     options=[{'label': br, 'value': br} for br in branches],
                     value=[],
                     multi=True,
                     disabled=False,
                     clearable=True,
                     searchable=True)], width={'size': 2, "offset": 0, 'order': 1}),

    ]),

    # table display with components to export data and sorting headers. Style_data table- styling values with colors
    dbc.Row([
        dbc.Col([html.H5('Project - Report', className='text-center'),
                 dash_table.DataTable(id='table-container', data=[],
                                      columns=[{"name": i, "id": i, 'type': 'numeric'} for i in df.columns],
                                      export_format="xlsx",
                                      sort_action='native',
                                      style_data_conditional=[
                                          {
                                              'if': {
                                                  'filter_query': '{Used Work/Work} < 1',
                                                  'column_id': 'Used Work/Work'
                                              },
                                              'color': 'red',
                                          },
                                          {
                                              'if': {
                                                  'filter_query': '{Used Work/Work} = 1',
                                                  'column_id': 'Used Work/Work'
                                              },
                                              'color': 'olive',
                                          },
                                          {
                                              'if': {
                                                  'filter_query': '{Used Work/Work} > 1',
                                                  'column_id': 'Used Work/Work'
                                              },
                                              'color': 'green',
                                          },
                                          {
                                              'if': {
                                                  'filter_query': '{Used Plan/Plan} < 1',
                                                  'column_id': 'Used Plan/Plan'
                                              },
                                              'color': 'red',
                                          },
                                          {
                                              'if': {
                                                  'filter_query': '{Used Plan/Plan} = 1',
                                                  'column_id': 'Used Plan/Plan'
                                              },
                                              'color': 'olive',
                                          },
                                          {
                                              'if': {
                                                  'filter_query': '{Used Plan/Plan} > 1',
                                                  'column_id': 'Used Plan/Plan'
                                              },
                                              'color': 'green',
                                          },
                                          {
                                              'if': {
                                                  'filter_query': '{Used Work/Used Plan} < 1',
                                                  'column_id': 'Used Work/Used Plan'
                                              },
                                              'color': 'red',
                                          },
                                          {
                                              'if': {
                                                  'filter_query': '{Used Work/Used Plan} = 1',
                                                  'column_id': 'Used Work/Used Plan'
                                              },
                                              'color': 'olive',
                                          },
                                          {
                                              'if': {
                                                  'filter_query': '{Used Work/Used Plan} > 1',
                                                  'column_id': 'Used Work/Used Plan'
                                              },
                                              'color': 'green',
                                          },
                                          {
                                              'if': {
                                                  'filter_query': '{Billable/Used Work} < 1',
                                                  'column_id': 'Billable/Used Work'
                                              },
                                              'color': 'red',
                                          },
                                          {
                                              'if': {
                                                  'filter_query': '{Billable/Used Work} = 1',
                                                  'column_id': 'Billable/Used Work'
                                              },
                                              'color': 'olive',
                                          },
                                          {
                                              'if': {
                                                  'filter_query': '{Billable/Used Work} > 1',
                                                  'column_id': 'Billable/Used Work'
                                              },
                                              'color': 'green',
                                          },
                                      ],
                                      style_table={'overflow': 'scroll', 'height': 500},
                                      style_header={'fontWeight': 'bold'},
                                      style_cell={'textAlign': 'center'})
                 ], width={'size': 12, "offset": 0, 'order': 1})
    ]),

    # html component of 5 graphs from fig to fig4
    dcc.Tabs([
        dcc.Tab(label='We are', children=[
            dcc.Graph(
                id='graph1',
                figure=fig
            )
        ]),
        dcc.Tab(label='Used Work vs Work', children=[
            dcc.Graph(
                id='graph2',
                figure=fig1
            )
        ]),
        dcc.Tab(label='Used Planed vs Plan', children=[
            dcc.Graph(
                id='graph3',
                figure=fig2
            )
        ]),
        dcc.Tab(label='Used Work vs Used Plan', children=[
            dcc.Graph(
                id='graph4',
                figure=fig3
            )
        ]),
        dcc.Tab(label='Billable vs Used Work', children=[
            dcc.Graph(
                id='graph5',
                figure=fig4
            )
        ])
    ])

])


# function: styling score color on graphs
def font_color(value: float) -> dict:
    font = dict(
        family="Roboto",
        size=15)
    if value < 1:
        font['color'] = "red"
    elif value == 1:
        font['color'] = "olive"
    else:
        font['color'] = "green"
    return font


# app callback for input and output data update on table and graphs for choice on filter of
# data and customer and project and user
@app.callback([Output('table-container', 'data'),
               Output('graph1', 'figure'),
               Output('graph2', 'figure'),
               Output('graph3', 'figure'),
               Output('graph4', 'figure'),
               Output('graph5', 'figure'),
               Output('filter_dropdown', 'options'),
               Output('project_dropdown', 'options')],
              [Input('my-date-picker-range', 'start_date'),
               Input('my-date-picker-range', 'end_date'),
               Input('filter_dropdown', 'value'),
               Input('project_dropdown', 'value'),
               Input('customer_dropdown', 'value')])
def update_data(selected_start_date, selected_end_date, selected_branches, projects, customers):
    # filter the data frame based on the DatePickerRange selection
    data = df[(df.index >= selected_start_date) & (df.index <= selected_end_date)]

    # filter the data frame based on the Dropdown selection

    if customers:
        data = data[data['Customer Name'].isin(customers)]
    # updated dropdown project list to updated data from chosen of filter customer
    branches6 = data['Project name'].sort_values(ascending=True).unique().tolist()
    projects2 = [{'label': br, 'value': br} for br in branches6]

    if projects:
        data = data[data['Project name'].isin(projects)]

    # updated dropdown project list to updated data from chosen of filter customer
    branches3 = data['user name'].sort_values(ascending=True).unique().tolist()
    users = [{'label': br, 'value': br} for br in branches3]

    if selected_branches:
        data = data[data['user name'].isin(selected_branches)]
    # update data from filter selection on graphs
    df3 = pd.DataFrame({"Hours": ["Used Work", "Work"], "Amount": [round(data['Used Work'].sum(), 2),
                                                                   round(data['Work'].sum(), 2)]})

    df4 = pd.DataFrame({"Hours": ["Used Planed", "Planed"], "Amount": [round(data['Used Plan'].sum(), 2),
                                                                       round(data['Plan'].sum(), 2)]})

    df5 = pd.DataFrame({"Hours": ["Used Work", "Used Planed"], "Amount": [round(data['Used Work'].sum(), 2),
                                                                          round(data['Used Plan'].sum(), 2)]})

    df7 = pd.DataFrame({"Hours": ['Billable', "Used Work"], "Amount": [round(data['Billable'].sum(), 2),
                                                                       round(data['Used Work'].sum(), 2)]})
    fig = go.Figure()
    fig.add_trace(go.Histogram(histfunc="count", x=data['user name']))

    fig1 = px.bar(df3, x="Hours", y="Amount", color="Hours", barmode="group", text="Amount")

    score1 = round(data['Used Work'].sum() / (data['Work'].sum()), 2)
    font = font_color(score1)

    fig1.add_annotation(text="Score: " + str(score1), xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False,
                        font=font)

    fig2 = px.bar(df4, x="Hours", y="Amount", color="Hours", barmode="group", text="Amount")
    score2 = round(data['Used Plan'].sum() / (data['Plan'].sum()), 2)

    font = font_color(score2)
    fig2.add_annotation(text="Score: " + str(score2), xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False,
                        font=font)

    fig3 = px.bar(df5, x="Hours", y="Amount", color="Hours", barmode="group", text="Amount")
    score3 = round(data['Used Work'].sum() / (data['Used Plan'].sum()), 2)
    font = font_color(score3)
    fig3.add_annotation(text="Score: " + str(score3), xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False,
                        font=font)

    fig4 = px.bar(df7, x="Hours", y="Amount", color="Hours", barmode="group", text="Amount")
    score4 = round(data['Billable'].sum() / (data['Used Work'].sum()), 2)

    font = font_color(score4)
    fig4.add_annotation(text="Score: " + str(score4), xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False,
                        font=font)

    return data.to_dict(orient='records'), fig, fig1, fig2, fig3, fig4, users, projects2


if __name__ == '__main__':
    app.run_server()
