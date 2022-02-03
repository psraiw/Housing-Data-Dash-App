import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State

str1 = ""
str2 = ""
data = pd.read_csv('housing.csv')
data = data.replace(' ', '_', regex=True)

#new columns
#added avgRooms, avgBedrooms, pop_per_household columns
data['avgRooms'] = data['total_rooms'] / data['households']
data['avgBedrooms'] = data['total_bedrooms'] / data['households']
data['pop_per_household'] = data['population'] / data['households']
columns = ['population','households','median_income','median_house_value','avgRooms','avgBedrooms','pop_per_household']

# app = dash.Dash(__name__)
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#html layout
app.layout = html.Div([
    html.Div([

        html.H2("Housing Data", style={'textAlign': 'center'}),
        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in columns],
                value='population'
            ),
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.H4(children='VS', style={'textAlign': 'center', 'display': 'inline-block' }),
        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in columns],
                value='households'
            ),
        ], style={'width': '48%', 'display': 'inline-block'}),
        
        html.H6("Select Proximity from Ocean : ", style={'inline-block':'inline-block'}),
        dcc.Checklist(
            id="ocean-proximity",
            options=[
                {"label": "Near Bay", "value": "NEAR_BAY"},
                {"label": "< 1H Ocean", "value": "<1H_OCEAN"},
                {"label": "Inland", "value": "INLAND"},
                {"label": "Near Ocean", "value": "NEAR_OCEAN"},
                {"label": "Island", "value": "ISLAND"},
            ],
            value=[],
            labelStyle={"display": "inline-block"},
        ),
        html.H6(str1, style={'textAlign': 'center'}, id="no-of-entries"),
        html.H4(str2, style={'textAlign': 'center' },id="grap-title"),
        dcc.Graph(id = "Housing-graph"),
        html.H6("Created by : Priyanshu Sawarkar", style={'textAlign': 'right', 'color': '#0099ff'})
        
    ])
])

#callback function
@app.callback(
    Output('Housing-graph', 'figure'),
    Output('no-of-entries', 'children'),
    Output('grap-title', 'children'),
    Input('xaxis-column', 'value'),
    Input('yaxis-column', 'value'),
    [Input("ocean-proximity", "value")])

def update_graph(xaxis_column_name, yaxis_column_name, ocean_proximity_options):
    
    df = data[data['ocean_proximity'].isin(ocean_proximity_options)]
    # print(df.info())
    fig = px.scatter(df, x=xaxis_column_name, y=yaxis_column_name,color=xaxis_column_name, hover_name=xaxis_column_name)
    no_entries = len(df)
    str1 = "no of entries : " + str(no_entries)
    str2 = f"Housing Data {xaxis_column_name} vs {yaxis_column_name}"
    return fig,str1,str2
    
    
if __name__ == '__main__':
    app.run_server(debug=True)