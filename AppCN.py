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
    html.H1(children='2019 Novel Coronavirus (2019-nCoV) Information Integration'),

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
        dcc.Tab(label='疫情数据+同程查询', value='tab-1'),
        dcc.Tab(label='WHO+CDC', value='tab-2'),
        dcc.Tab(label='资源信息', value='tab-3')
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
                        width=1200),

            html.Iframe(children='DXY',
                        src="https://2019.ncov.wtf/",
                        height=550,
                        width=600),

            html.Iframe(children='同程查询',
                        src="https://sa.sogou.com/new-weball/page/sgs/epidemic/yyxw?type_page=yangshi&from=singlemessage&isappinstalled=0",
                        height=550,
                        width=600)
        ])

    elif tab == 'tab-2':
        return html.Div([
            html.Div(children='''WHO'''),
            html.Iframe(children='WHO',
                        src="https://www.who.int/emergencies/diseases/novel-coronavirus-2019/situation-reports",
                        height=500,
                        width=1250),

            html.Div(children='''CDC'''),
            html.Iframe(children='CDC',
                        src="http://www.chinacdc.cn/jkzt/crb/zl/szkb_11803/",
                        height=500,
                        width=1250)
        ])

    elif tab == 'tab-3':
        return html.Div([
            html.Div(children='''义诊信息'''),
            html.Iframe(children='义诊信息',
                        src="https://shimo.im/sheets/JgXjYCJJTRQxJ3GP/MODOC/",
                        height=500,
                        width=1250),

            html.Div(children='''医院物资'''),
            html.Iframe(children='医院物资',
                        src="https://shimo.im/sheets/k399pHyt6HKvW6xR/MODOC/",
                        height=500,
                        width=1250),

            html.Div(children='''捐赠渠道'''),
            html.Iframe(children='捐赠渠道',
                        src="https://shimo.im/sheets/W3gxW6cwkYTDY6DD/",
                        height=500,
                        width=1250),

            html.Div(children='''物资生产'''),
            html.Iframe(children='物资生产',
                        src="https://shimo.im/sheets/pchvJ6ddyRHHdXtv/MODOC/",
                        height=500,
                        width=1250),

            html.Div(children='''物流信息'''),
            html.Iframe(children='物流信息',
                        src="https://shimo.im/sheets/RTHXp3ghtKXY3GcC/MODOC/",
                        height=500,
                        width=1250)
        ])

if __name__ == '__main__':
    app.run_server(debug=True)