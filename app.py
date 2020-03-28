import dash
import dash_core_components as dcc
import dash_html_components as html

#print(dash_core_components.__version__)

# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div(children=[
    html.H1(children='COVID-19 Information Integration'),

    html.Div(children='''
        Author: Dylan Shen 
    '''),

    html.Div(children='''
        Github: https://github.com/Dylansppy/2019-nCov 
    '''),

    html.Div(children='''
        LinkedIn: https://www.linkedin.com/in/dylan-shen-peng
    '''),

    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Pandemic Situation', value='tab-1'),
        dcc.Tab(label='Ministry of Health', value='tab-2'),
        dcc.Tab(label='Other Resources', value='tab-3')
    ]),

    html.Div(id='tabs-content')

    #dcc.Graph(
        #id='example-graph',
        #figure={
            #'data': [
                #{'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                #{'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            #],
            #'layout': {
                #'title': 'Dash Data Visualization'
            #}
        #}
    #)
])

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])

def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.Iframe(children='JHU',
                        src="https://gisanddata.maps.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6",
                        height=500,
                        width=1200)
        ])

    elif tab == 'tab-2':
        return html.Div([
            html.Div(children='''Ministry of Health'''),
            html.A("Ministry of Health", href='https://www.health.govt.nz/our-work/diseases-and-conditions/covid-19-novel-coronavirus', target="_blank")
        ])

    elif tab == 'tab-3':
        return html.Div([
            html.Div(children='''WHO'''),
            html.Iframe(children='WHO',
                        src="https://www.who.int/emergencies/diseases/novel-coronavirus-2019/situation-reports",
                        height=500,
                        width=1250),

            html.Div(children='''CDC'''),
            html.Iframe(children='CDC',
                        src="https://www.cdc.gov/coronavirus/2019-ncov/index.html",
                        height=500,
                        width=1250)
        ])

if __name__ == '__main__':
    app.run_server(debug=True)