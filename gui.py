#DFP project
#Interface
#Author: Yuwei Zhu

##############################
#import modules
import plotly as py
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import data_analyze as da
import cluster as Cluster

#input data
input = pd.read_csv('clean_all.csv')
del input['Unnamed: 0']

#create data frame for analysis
df = da.Data(input)#whole table
group_df = da.GroupData(input)#group by Neighborhood
major_group_feature = group_df.feature_names()
neighbor_list = group_df.get_index()

#cluster result
cluster_result = Cluster.cluster_result()
neighbors,clusters = [],[]
for key,value in cluster_result.items():
    neighbors.append(key)
    clusters.append(str(value))

app = dash.Dash()


app.layout =  html.Div([
                html.H1('The Nextdoor',style={'color':'rgb(192,72,81)','margin-left':'550px',
                                              'font-size':'40px','font-family':'arial'}),
                html.H2('Get to know the neighborhood!',style={'color':'rgb(192,72,81)','margin-left':'520px'}),
#sort neighborhood based on selected feature
                html.Div([
                    html.H2('Sort Neighborhood by feature ', style={'color':'rgb(23,114,180)','margin-left':'120px'}),
                    dcc.Dropdown(
                        id = 'dropdown-a',
                        options=[
                            {'label': i, 'value': i} for i in major_group_feature
                                ],
                        value='Sectors',
                    style={'margin-top' :'60px'}),
                    dcc.Graph(id = 'sort_graph',style={'margin-top':'120px'})
                       ],
                    style={'width': '45%', 'height':'700px','float': 'left','margin-left':'20px'}),
#compate two neighborhood
                html.Div([
                    html.H2('Compare two neighborhoods ',style={'color' :'rgb(69,183,135)','margin-left':'200px'}),
                    html.H4('Neighborhood 1: ',style={'margin-left':'50px','margin-right':'50px'}),
                    dcc.Dropdown(
                        id = 'dropdown-b',
                        options=[{'label': i, 'value': i} for i in neighbor_list],
                        value='Arlington',style={'margin-left':'25px','margin-right':'50px'}),
                    html.H4('Neighborhood 2: ',style={'margin-left':'50px','margin-right':'50px'}),
                    dcc.Dropdown(
                        id = 'dropdown-c',
                        options=[
                            {'label': i, 'value': i} for i in neighbor_list
                                ],
                        value='Arlington',style={'margin-left':'25px','margin-right':'50px'}),
                    html.Div(id = 'two_price', style={'color':'rgb(160,90,0)', 'font-size':'20px',
                                                      'margin-top': '20px','margin-left':'50px'}),
                    dcc.Graph(id = 'compare_graph')
                       ],
                    style={'width': '50%', 'float': 'left','margin-right':'20px'}),
#recommendation based on cluster result
                html.Div([
                    html.H2('Similar Neighborhoods Recommendation',style={'color':'rgb(254,215,26)'}),
                    html.H4('Neighborhood that interests you: '),
                    dcc.Dropdown(
                        id = 'dropdown-f',
                        options=[
                            {'label': i, 'value': i} for i in neighbor_list
                                ],
                        value='Arlington'),
                    html.Div(id='similar_neighborhood',
                             style={'color': 'violet', 'font-size': '20px',
                                    'margin-top':'20px'})
                ],style={'margin-left':'100px','margin-right':'100px','margin-top':'800px'}),
#select feature to plot cluster result
                html.Div([
                    html.H2('Visualizae Similar Neighborhoods Features',style={'color':'rgb(120,70,20)'}),
                    html.H4('Feature 1: '),
                    dcc.Dropdown(
                        id = 'dropdown-d',
                        options=[{'label': i, 'value': i} for i in major_group_feature],
                        value='Sectors'),
                    html.H4('Feature 2: '),
                    dcc.Dropdown(
                        id = 'dropdown-e',
                        options=[{'label': i, 'value': i} for i in major_group_feature],
                        value='Price'),
                    dcc.Graph(id = 'cluster_graph',style={'margin-left':'50px','margin-right':'50px','height':'600px'})
                ],style={'margin-left':'100px','margin-right':'100px','margin-top':'50px'})
    ])


#this method drawing sorted graph
########################################
#Helper functions to draw group sorted graph
def sort_graph(feature):
    group_df.sort(feature)#first sort the data frame
    ne = group_df.get_index() #get neighborhood name
    col_value = group_df.get_value(feature)
    return ne,col_value

@app.callback(dash.dependencies.Output('sort_graph', 'figure'),
             [dash.dependencies.Input('dropdown-a', 'value')])

def update_figure1(input_data):
    x1, x2 = sort_graph(input_data)
    return {
        'data': [{'x': x1,'y': x2, 'type': 'line'}],
        'layout': go.Layout({'title': 'Neighborhood sorted by ' + str(input_data)}
        )
    }

##########################################
#method to compare two neighborhoods
def city_average():
    city_avg = df.mean()
    return city_avg

def get_bar_value(neighbor1,neighbor2):
    value1, feature1 = group_df.get_row_bar(neighbor1)
    value2, feature2 = group_df.get_row_bar(neighbor2)
    return value1,value2, feature1

#list house prices for two neighborhood
@app.callback(dash.dependencies.Output('two_price', 'children'),
             [dash.dependencies.Input('dropdown-b', 'value'),
              dash.dependencies.Input('dropdown-c', 'value')])

def update_price(neighbor1, neighbor2):
    price1 = round(group_df.get_single_value_bar('Price',neighbor1),0)
    price2 = round(group_df.get_single_value_bar('Price',neighbor2),0)
    return 'House Price of {} is ${}; House Price of {} is ${}'.format(neighbor1,price1,neighbor2,price2)

#draw bar chart
@app.callback(dash.dependencies.Output('compare_graph', 'figure'),
             [dash.dependencies.Input('dropdown-b', 'value'),
              dash.dependencies.Input('dropdown-c', 'value')])

def update_figure2(neighbor1, neighbor2):
    value1,value2,feature = get_bar_value(neighbor1,neighbor2)
    avg = city_average()
    trace1 = go.Bar(
        x = feature,
        y = value1,
        name = neighbor1
    )
    trace2 = go.Bar(
        x=feature,
        y=value2,
        name=neighbor2
    )
    data = [trace1, trace2]
    return {'data': data,
            'layout' : go.Layout({'title': 'Compare two neighborhoods'})}

#return similar neighborhood
#helper function create cluster dict mapping to neighborhood
def cluster_dict():
    cluster_dict = {}
    for key, value in cluster_result.items():
        if value in cluster_dict:
            cluster_dict[value] += [key]
        else:
            cluster_dict[value] = [key]
    return cluster_dict

@app.callback(dash.dependencies.Output('similar_neighborhood', 'children'),
             [dash.dependencies.Input('dropdown-f', 'value')])

def update_recommendation(input):
    dict = cluster_dict()
    result = -1
    for key, value in dict.items():
        if input in value:
            result = key
    recommendation = dict[result]
    return 'Similar neighborhoods are: {}'.format(recommendation)


#draw cluster result plot
#helper function to get value of selected features

rainbow_colorscale =  \
    [
    'beige', 'darkblue',
    'gold', 'red',
    'maroon', 'green',
    'black', 'pink'
    ]

def cluster_color():
    color_dict = {}
    unique_cluster = list(set(clusters))
    for i in range(len(unique_cluster)):
        color_dict[i] = rainbow_colorscale[i]
    return color_dict


@app.callback(dash.dependencies.Output('cluster_graph', 'figure'),
             [dash.dependencies.Input('dropdown-d', 'value'),
              dash.dependencies.Input('dropdown-e', 'value')])

def update_figure3(feature1, feature2):
    value1 = group_df.get_value(feature1)
    value2 = group_df.get_value(feature2)
    color = cluster_color()

    #create a list with neighborhood and feature values as value
    match_list = []
    for i, neighbor in enumerate(neighbors):
        new = [neighbor, value1[i], value2[i]]
        match_list.extend([new])

    #create a dict with cluster number as key
    cluster_dict1 = {}
    for i in range(len(match_list)):
        ne = match_list[i][0]
        value1 = match_list[i][1]
        clu = cluster_result[ne]
        if clu in cluster_dict1:
            cluster_dict1[clu] += [value1]
        else:
            cluster_dict1[clu] = [value1]

    cluster_dict2 = {}
    for i in range(len(match_list)):
        ne = match_list[i][0]
        value2 = match_list[i][2]
        clu = cluster_result[ne]
        if clu in cluster_dict2:
            cluster_dict2[clu] += [value2]
        else:
            cluster_dict2[clu] = [value2]

    cluster_dict_neigbor = {}
    for i in range(len(match_list)):
        ne = match_list[i][0]
        clu = cluster_result[ne]
        if clu in cluster_dict_neigbor:
            cluster_dict_neigbor[clu] += [ne]
        else:
            cluster_dict_neigbor[clu] = [ne]

    trace = []
    for i, key in enumerate(cluster_dict1):
        x = cluster_dict1[key]
        y = cluster_dict2[key]
        ne = cluster_dict_neigbor[key]
        col = color[key]
        trace.append(go.Scatter(
            x = x,
            y = y,
            text = ne,
            mode = 'markers',
            opacity = 0.7,
            marker = {
                'size': 15,
                'color': col,
                'line': {'width': 0.5, 'color': 'white'}},
            name = 'cluster'+str(i)
        ))
    return { 'data': trace,
            'layout': go.Layout({'title': 'Neighborhood Cluster',
                                 'xaxis' : {'title':feature1},
                                 'yaxis' : {'title':feature2}})}


if __name__ == '__main__':
    app.run_server(debug = True)