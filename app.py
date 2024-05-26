import pandas as pd
import numpy as np 
import plotly.graph_objects as go 
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output

external_stylesheets = [
    {
        'href':"https://cdn.jsdelivr.net/npm/bootstrap@4.1.3/dist/css/bootstrap.min.css",
        'rel':"stylesheet",
        'integrity':'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin':"anonymous"
    }
]

df = pd.read_csv('/home/swasti/Desktop/covid_19/IndividualDetails.csv')

total_patients = df.shape[0]
active = df[df['current_status']=='Hospitalized'].shape[0]
recovered = df[df['current_status']=='Recovered'].shape[0]
death = df[df['current_status']=='Deceased'].shape[0]
migrate = df[df['current_status']=='Migrated'].shape[0]

option = [
    {'label':'All', 'value':'All'},
    {'label':'Hospitalized', 'value':'Hospitalized'},
    {'label':'Recovered', 'value':'Recovered'},
    {'label':'Deceased', 'value':'Deceased'},
    {'label':'Migrated', 'value':'Migrated'}
]

app = dash.Dash(__name__,external_stylesheets=external_stylesheets)

app.layout=html.Div([
    html.H1("Covid",style={'text-align':'center', 'padding':'40px 0 30px 0'}),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H4('Total Cases'),
                    html.H5(total_patients),
                ],className='card-body',style={'text-align':'center'})
            ],className='card')
        ],className='col-md-2'),
        html.Div([
            html.Div([
                html.Div([
                    html.H4('Active'),
                    html.H5(active),
                ],className='card-body',style={'text-align':'center'})
            ],className='card')
        ],className='col-md-2'),
        html.Div([
            html.Div([
                html.Div([
                    html.H4('Recovered'),
                    html.H5(recovered),
                ],className='card-body',style={'text-align':'center'})
            ],className='card')
        ],className='col-md-2'),
        html.Div([
            html.Div([
                html.Div([
                    html.H4('Deaths'),
                    html.H5(death),
                ],className='card-body',style={'text-align':'center'})
            ],className='card')
        ],className='col-md-2'),
        html.Div([
            html.Div([
                html.Div([
                    html.H4('Migrated'),
                    html.H5(migrate),
                ],className='card-body',style={'text-align':'center'})
            ],className='card')
        ],className='col-md-2'),
    ],className='row' , style={'justify-content':'center', 'padding': '0 0 25px 0 '}),
    html.Div([],className='row'),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(id="picker", options=option, value="All"),
                    dcc.Graph(id='bar')
                ], className='card-body')
            ], className='card')
        ], className='col-md-12')
    ],className='row')
], className='container')
'''call back fun on app output given to id bar and output is figure parameter 
and input is taken from id picker and input value is value '''
@app.callback(Output('bar', 'figure'), [Input('picker', 'value')])
def update_graph(type):

    if type == 'All':
        pbar = df['detected_state'].value_counts().reset_index()
        pbar.columns = ['State', 'Count']
        return {
            'data':[go.Bar(x=pbar['State'], y=pbar['Count'])],
            'layout':go.Layout(title='State Total Count')
        }
    else:
        npat = df[df['current_status']==type]
        pbar = npat['detected_state'].value_counts().reset_index()
        pbar.columns = ['State', 'Count']
        return {
            'data':[go.Bar(x=pbar['State'], y=pbar['Count'])],
            'layout':go.Layout(title='State Total Count')
        }

if __name__=='__main__':
    app.run_server(debug=True)