import os
import dash
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP]) 
server = app.server




df = pd.read_excel("assets/dashboard.xlsx")




states = df.State.unique().tolist()
dates = df.Date
maxd = dates.max()
mind = dates.min()
outcome = df.Outcome.unique().tolist()
outcome.insert(0, "all")

def q1():
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=totsuc.index,y=totsuc.values,name="Success",line=dict(color='blue', width=2)))
    fig1.add_trace(go.Scatter(x=totnsuc.index,y=totnsuc.values,name= "Failure",line=dict(color='red', width=2)))
    fig1.add_trace(go.Scatter(x=tottime.index,y=tottime.values,name= "Time out",line=dict(color='green', width=2)))
    fig1.update_layout(title='Number of calls type as a function of date',
                   xaxis_title='Date',
                    yaxis_title='Number')

    if outcome == "all" :  
        fig1.add_trace(go.Scatter(x=totac.index, y=totac.values, name="Total",line=dict(color='#4744ff', width=2)))
        fig1.add_trace(go.Scatter(x=totsuc.index,y = totsuc.values*100/totac[totsuc.index],name = "Success Total Ratio",line=dict(color='orange', width=2))) 
    return fig1


def q2():
    fig2=go.Figure(data=[
    go.Bar(name="Success", x=totsucs.index, y=totsucs.values),
    go.Bar(name="Failure", x=totnsucs.index, y=totnsucs.values)
    ])
    fig2.update_layout(barmode='group', title='Number of success and failure calls by states', 
                        xaxis_title='State',
                        yaxis_title='Number')
    return fig2

def q3():
    fig3 = px.pie(values= df_outcome.values, names = df_outcome.index)
    return fig3


def q4():
    figure = go.Figure()
    totac = df.groupby("State")["Outcome"].count()
    totsuc = df[df["Outcome"] == "Success"].groupby("State")["Outcome"].count()
    state_success = (totsuc / totac * 100).sort_values(ascending=False)

    figure.add_trace(
        go.Bar(
            x=state_success.index,
            y=state_success.values,
            name="Number of success calls per state",
        )
    )
    

    figure["layout"]["xaxis"]["title"] = "State"
    figure["layout"]["yaxis"]["title"] = "Number of calls"
   

    return figure

def q5():
    figure = go.Figure()

    totac = df.groupby("State")["Outcome"].count()
    totsuc = df[df["Outcome"] == "Success"].groupby("State")["Outcome"].count()

    figure.add_trace(
        go.Pie(
            labels=totac.index,
            values=totac.values,
            textinfo="none",
            name="total calls",
            hole=0.8,
        ),
    )

    figure.add_trace(
        go.Pie(
            labels=totsuc.index,
            values=totsuc.values,
            textinfo="none",
            name="success calls",
            hole=0.65,
        ),
    )
    figure.data[0].domain = {"x": [0, 1], "y": [1, 1]}
    figure.data[1].domain = {"x": [0, 1], "y": [0.22, 0.78]}
    figure.update_traces(hoverinfo="label+percent+name")

    figure["layout"][
        "title"
    ] = "The total number of actions/ State and number of success / state ."
    figure["layout"]["legend_title"] = "Labels"

    return figure

def q6():
    try:
        fig6 = px.bar(df1_modify, x=df1_modify.Time_Period,
                      y=df1_modify.Outcome)
        return fig6
    except Exception as e:
        pass



def filter_date(outcome, state, start_date, end_date):
    global df, totac, totacs, totnsuc, totsucs, tottime, totnsucs, totsuc, df1_modify, df_outcome
    df = pd.read_excel("assets/dashboard.xlsx")
    if outcome == "all" and state == "all":
        df = df[(df.Date >= start_date) & (df.Date <= end_date)]
    elif outcome == "all":
        df = df[(df.Date >= start_date) & (df.Date <= end_date)]
        df = df[df.State.isin(state)]
    elif state == "all":
        df = df[(df.Date >= start_date) & (df.Date <= end_date)]
        df = df[df.Outcome.isin(outcome)]
    else:
        df = df[(df.Date >= start_date) & (df.Date <= end_date)]
        df = df[df.State.isin(state)]
        df = df[df.Outcome.isin(outcome)]
    totac = df.groupby('Date')['Outcome'].count()
    totsuc = df[df['Outcome'] == 'Success'].groupby('Date')['Outcome'].count()
    totnsuc = df[df['Outcome'] == 'Failure'].groupby('Date')['Outcome'].count()
    tottime = df[df['Outcome'] == 'Time out'].groupby('Date')[
        'Outcome'].count()
    totacs = df.groupby('State')['Outcome'].count()
    totsucs = df[df['Outcome'] == 'Success'].groupby('State')[
        'Outcome'].count()
    totnsucs = df[df['Outcome'] == 'Failure'].groupby('State')[
        'Outcome'].count()
    df_outcome = df.groupby("Outcome")["Outcome"].count()

    df1_modify = (
        df[df["Outcome"] == "Success"]
        .groupby("Time_Period")["Outcome"]
        .count()
        .reset_index()
    )

def filter2_date(state, start_date, end_date):
    global df, totac, totacs, totnsuc, totsucs, tottime, totnsucs, totsuc, df1_modify, df_outcome
    df = pd.read_excel("assets/dashboard.xlsx")
    if state == "all":
        df = df[(df.Date >= start_date) & (df.Date <= end_date)]
        df = df[df.Outcome.isin(outcome)]
    else:
        df = df[(df.Date >= start_date) & (df.Date <= end_date)]
        df = df[df.State.isin(state)]
    totac = df.groupby('Date')['Outcome'].count()
    totsuc = df[df['Outcome'] == 'Success'].groupby('Date')['Outcome'].count()
    totnsuc = df[df['Outcome'] == 'Failure'].groupby('Date')['Outcome'].count()
    tottime = df[df['Outcome'] == 'Time out'].groupby('Date')[
        'Outcome'].count()
    totacs = df.groupby('State')['Outcome'].count()
    totsucs = df[df['Outcome'] == 'Success'].groupby('State')[
        'Outcome'].count()
    totnsucs = df[df['Outcome'] == 'Failure'].groupby('State')[
        'Outcome'].count()
    df_outcome = df.groupby("Outcome")["Outcome"].count()

    df1_modify = (
        df[df["Outcome"] == "Success"]
        .groupby("Time_Period")["Outcome"]
        .count()
        .reset_index()
    )

def filter3_date(start_date, end_date):
    global df, totac, totacs, totnsuc, totsucs, tottime, totnsucs, totsuc, df1_modify, df_outcome
    df = pd.read_excel("assets/dashboard.xlsx")
    
    df = df[(df.Date >= start_date) & (df.Date <= end_date)]
    
    totac = df.groupby('Date')['Outcome'].count()
    totsuc = df[df['Outcome'] == 'Success'].groupby('Date')['Outcome'].count()
    totnsuc = df[df['Outcome'] == 'Failure'].groupby('Date')['Outcome'].count()
    tottime = df[df['Outcome'] == 'Time out'].groupby('Date')[
        'Outcome'].count()
    totacs = df.groupby('State')['Outcome'].count()
    totsucs = df[df['Outcome'] == 'Success'].groupby('State')[
        'Outcome'].count()
    totnsucs = df[df['Outcome'] == 'Failure'].groupby('State')[
        'Outcome'].count()
    df_outcome = df.groupby("Outcome")["Outcome"].count()

    df1_modify = (
        df[df["Outcome"] == "Success"]
        .groupby("Time_Period")["Outcome"]
        .count()
        .reset_index()
    )

header_component = html.H1("Calls Analysis Dashboard", style={"backgroundColor": "royalblue", "color": "white"  })

#  Set up layout
app.layout=html.Div(
    className="p-3 bg-gray",
    children=[
    dbc.Row(
        [header_component]
    ),

    dbc.Row( [
        dbc.Col([
             html.P("a-Success, failure, timedout calls per date.",
               style={'textAlign': 'center', "padding": "10px", "fontSize": "20px", "backgroundColor": "#4744ff", "color": "beige", "margin": "0px -12px", "borderTopLeftRadius": "8px", "borderTopRightRadius": "8px", "marginBottom":"30px"}),

        html.Div(children=[
            html.Div(
                children=[
                    dcc.Dropdown(
                        options=outcome,
                        multi = True,
                        id="input1",
                    ),
                ],
                className="col-3"
            ),
            html.Div(
                children=[
                    dcc.Dropdown(states,
                         multi=True,
                         value='all',
                         placeholder="all",
                         id="input2",
                    
                         ),
                ],
                className="col-3"
            ),
            html.Div(
                children=[
                    dcc.DatePickerRange(
                        end_date_placeholder_text='M-D-Y-Q',
                        id="input3",
                        start_date=mind,
                        end_date=maxd,
                        min_date_allowed=mind,
                        max_date_allowed=maxd,
                        
                    )
                ],
                className="col-6"
            ),
            
            
            ],
            className="dropdown1 row"),

        dcc.Graph(id="output1"),


        ],
        className="card m-2 shadow"), 
        dbc.Col(
            [
                html.P("b-Success and failure by State bargraph.", style={
               'textAlign': 'center', "padding": "10px", "fontSize": "20px", "backgroundColor": "#4744ff", "color": "beige", "margin": "0px -12px", "borderTopLeftRadius": "8px", "borderTopRightRadius": "8px", "marginBottom":"30px"}),


        html.Div(children=[
            html.Div(
                children=[
                    dcc.Dropdown(
                        options=["Success", "Failure"],
                        multi=True,
                        id="input4"),
                ],
                className="col-3"
            ),
            html.Div(
                children=[
                    dcc.Dropdown(states,
                         multi=True,
                         value='all',
                         placeholder="all",
                         id="input5"),
                ],
                className="col-3"
            ),
            html.Div(
                children=[
                    dcc.DatePickerRange(
                        end_date_placeholder_text='M-D-Y-Q',
                        id="input6",
                        start_date=mind,
                        end_date=maxd,
                        min_date_allowed=mind,
                        max_date_allowed=maxd,
                    )
                ],
                className="col-6"
            ),
            
            
            ],
            className="dropdown1 row"),

        dcc.Graph(id="output2"),
            ],className="card m-2 shadow")
            ]),
    dbc.Row(
        [dbc.Col(
            [
                html.P("c-Failure-success-timeout piechart.",
               style={'textAlign': 'center', "padding": "10px", "fontSize": "20px", "backgroundColor": "#4744ff", "color": "beige", "margin": "0px -12px", "borderTopLeftRadius": "8px", "borderTopRightRadius": "8px", "marginBottom":"30px"}),
        html.Div(children=[
            html.Div(
                children=[
                    dcc.Dropdown(states,
                         multi=True,
                         value='all',
                         placeholder="all",
                         id="input7"),
                ],
                className="col-6"
            ),
            html.Div(
                children=[
                    dcc.DatePickerRange(
                        end_date_placeholder_text='M-D-Y-Q',
                        id="input8",
                        start_date=mind,
                        end_date=maxd,
                        min_date_allowed=mind,
                        max_date_allowed=maxd,
                    ),
                ],
                className="col-6"
            ),
            
            ], className="dropdown1 row"),
            dcc.Graph(id="output3"),
            ]
            ,className="card m-2 shadow"
        ), 
        dbc.Col([
            html.P("e-Total number of actions/state and number of success/state.", style={
               'textAlign': 'center', "padding": "10px", "fontSize": "20px", "backgroundColor": "#4744ff", "color": "beige", "margin": "0px -12px", "borderTopLeftRadius": "8px", "borderTopRightRadius": "8px", "marginBottom":"30px"}),
        html.Div(children=[
            html.Div(
                children=[
                    dcc.Dropdown(states,
                         multi=True,
                         value='all',
                         placeholder="all",
                         id="input10"),
                ],
                className="col-6"
            ),

            html.Div(
                children=[
                    dcc.DatePickerRange(
                        end_date_placeholder_text='M-D-Y-Q',
                        id="input11",
                        start_date=mind,
                        end_date=maxd,
                        min_date_allowed=mind,
                        max_date_allowed=maxd,
                    ),
                ],
                className="col-6"
            ),
            ], className="dropdown1 row"),
            dcc.Graph(id="output5")]
            ,className="card m-2 shadow"
            
        )
        ]
    ),
    dbc.Row(
        [dbc.Col(
            [
            html.P("d-The most 'successful' state in terms of the share ratios.", style={
               'textAlign': 'center', "padding": "10px", "fontSize": "20px", "backgroundColor": "#4744ff", "color": "beige", "margin": "0px -12px", "borderTopLeftRadius": "8px", "borderTopRightRadius": "8px", "marginBottom":"30px"}),
            html.Div(children=[

           

            dcc.DatePickerRange(
                end_date_placeholder_text='M-D-Y-Q',
                id="input9",
                start_date=mind,
                end_date=maxd,
                min_date_allowed=mind,
                max_date_allowed=maxd,
            ),
            ], className="dropdown1"),
            dcc.Graph(id="output4")]
            ,className="card m-2 shadow"
        ), 
        dbc.Col(
            [
                
            html.P("f-The number of the success calls by Time_Period", style={
               'textAlign': 'center', "padding": "10px", "fontSize": "20px", "backgroundColor": "#4744ff", "color": "beige", "margin": "0px -12px", "borderTopLeftRadius": "8px", "borderTopRightRadius": "8px", "marginBottom":"30px"}),
        html.Div(children=[
            html.Div(
                children=[
                     dcc.Dropdown(states,
                         multi=True,
                         value='all',
                         placeholder="all",
                         id="input12"),
                ],
                className="col-6"
            ),

            html.Div(
                children=[
                    dcc.DatePickerRange(
                        end_date_placeholder_text='M-D-Y-Q',
                        id="input13",
                        start_date=mind,
                        end_date=maxd,
                        min_date_allowed=mind,
                        max_date_allowed=maxd,
                    ),
                ],
                className="col-6"
            ),
           
           
            ], className="dropdown1 row"),
            dcc.Graph(id="output6")
            ],className="card m-2 shadow"
        )
        ]),
])


# Dropdown 1
@ app.callback(
    Output('output1', 'figure'),
    Input('input1', "value"),
    Input('input2', "value"),
    Input('input3', "start_date"),
    Input('input3', "end_date"),
)

def update_output(value1, value2, value3, value4):
    if value2 == None or len(value2) == 0:
        value2 = "all"
    if value1 == None or len(value1) == 0:
        value1 = "all"
    filter_date(value1, value2, value3, value4)
    return q1()


#Dropdown2
@ app.callback(
    Output('output2', 'figure'),
    Input('input4', "value"),
    Input('input5', "value"),
    Input('input6', "start_date"),
    Input('input6', "end_date"),
)
def update_output(value1, value2, value3, value4):

    if value2 == None or len(value2) == 0:
        value2 = "all"

    if value1 == None or len(value1) == 0:
        value1 = "all"

    filter_date(value1, value2, value3, value4)
    return q2()


#Drowpdown3
@app.callback(
    Output('output3', 'figure'),
    [Input('input7', "value"),
    Input('input8', "start_date"),
    Input('input8', "end_date"),],
)

def update_output(value1, value2, value3):

    if value2 == None or len(value2) == 0:
        value2 = "all"

    if value1 == None or len(value1) == 0:
        value1 = "all"

    filter2_date(value1, value2, value3)

    return q3()


#Dropdown5
@ app.callback(
    Output('output5', 'figure'),
    Input('input10', "value"),
    Input('input11', "start_date"),
    Input('input11', "end_date"),
)
def update_output(value1, value2, value3):

    if value2 == None or len(value2) == 0:
        value2 = "all"

    if value1 == None or len(value1) == 0:
        value1 = "all"

    filter2_date(value1, value2, value3)

    return q5()


#Drowpdown4
@ app.callback(
    Output('output4', 'figure'),
    Input('input9', "start_date"),
    Input('input9', "end_date"),
)
def update_output(value1, value2):

    if value1 == None or len(value1) == 0:
        value1 = "all"

    filter3_date(value1, value2)

    return q4()

@ app.callback(
    Output('output6', 'figure'),
    Input('input12', "value"),
    Input('input13', "start_date"),
    Input('input13', "end_date"),
)
def update_output(value1, value2, value3):

    if value2 == None or len(value2) == 0:
        value2 = "all"

    if value1 == None or len(value1) == 0:
        value1 = "all"

    filter2_date(value1, value2, value3)

    return q6()



#run local server

if __name__ == "__main__":
    app.run_server("0.0.0.0", debug=False, port=int(
        os.environ.get('PORT', 8000)))
