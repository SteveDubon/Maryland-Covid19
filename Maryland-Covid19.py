import pandas as pd

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import plotly.graph_objs as go
import plotly.express as px

from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)


#==============================================DATA=====================================================================
#USA COVID19 DEATHS
df_US_deaths = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv')

df = df_US_deaths                                                                                                       #Create copy of DF

df['January Total'] = df.loc[:, '1/22/20' : '1/31/20'].sum(axis=1)                                                      #Add the total deaths per month
df['February Total'] = df.loc[:, '2/1/20' : '2/29/20'].sum(axis=1)
df['March Total'] = df.loc[:, '3/1/20' : '3/31/20'].sum(axis=1)
df['April Total'] = df.loc[:, '4/1/20' : '4/30/20'].sum(axis=1)
df['May Total'] = df.loc[:, '5/1/20' : '5/31/20'].sum(axis=1)
df['June Total'] = df.loc[:, '6/1/20' : '6/30/20'].sum(axis=1)
df['July Total'] = df.loc[:, '7/1/20' : '7/28/20'].sum(axis=1)

#print(df.head())
#print(list(df.columns))
#print(df['FIPS'].head(200))

df = df.loc[82:3223 , :].reset_index(drop=True)                                                                         #Clean (only 50 states)

df['FIPS'] = df['FIPS'].astype('int64')                                                                                 #Fix DIPS col (5 digits total)
df['FIPS'] = df['FIPS'].apply(lambda x: str(x).zfill(5))
#print(df['FIPS'].tail())
#print(df.loc[3139:3141, :'Province_State'])

#print(df.loc[1193:1216, 'Province_State':])

# #============================================MAP INFORMATION=============================================================
colorscale = ["#d9feff", "#b0fdff", "#87fcff", "#63fbff", "#38faff", "#1ff9ff", "#fa8ebb", "#ff69a7"]


# fips = df['FIPS'].tolist()
# values = df['January Total'].tolist()

#endpts = list(np.linspace(1, 12, len(colorscale) - 1))

token = 'pk.eyJ1Ijoic3RldmVkdWJvbiIsImEiOiJja2Nxa3FkdjYwbXc1MnJvY3RqdjJyejR6In0.heuPS8EqIj3W7yYElk-XYw'
map_style = 'mapbox://styles/stevedubon/ckcqli1u404911hnv136abnbs'

#============================================START DASH APP=============================================================
#Start the App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

#==============================================APP LAYOUT===============================================================
#App layout
app.layout = html.Div([
    html.Hr(),
    dbc.Row(

        dbc.Col(
            [
                html.H4("Impact of COVID-19 on the State of Maryland", className="card-title"),
                html.H6("January - July", className="card-subtitle"),

                html.Hr(),

                html.P(
                    "Deaths are classified using the data repository for the 2019 Novel Coronavirus Visual Dashboard \
                    operated by the Johns Hopkins University Center for Systems Science and Engineering (JHU CSSE). \
                    Also, Supported by ESRI Living Atlas Team and the Johns Hopkins University Applied Physics Lab (JHU APL).",
                    className="card-text",
                ),

                dbc.CardLink("Data Repository", href="https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv"),
                dbc.CardLink("Inspired By", href="https://dash-gallery.plotly.host/dash-opioid-epidemic/"),
            ], width={"size": 10, "offset": 1}
        ),

    ),

    html.Hr(),


#-----------------------------------------------------------------------------------------------------------------------
    dbc.Row(
        [
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        dbc.Col(
                            html.H5("Impact of COVID-19 per month:", className="card-title"), width={"size": 8, "offset": 3}
                        ),

                        dcc.Slider(id='month_slider',
                                    min=1,
                                    max=7,
                                    value=4,
                                    marks={1: 'Jan',
                                           2: 'Feb',
                                           3: 'Mar',
                                           4: 'Apr',
                                           5: 'May',
                                           6: 'Jun',
                                           7: 'Jul'},
                                    step=1,
                        ),

                        html.Hr(),
                        html.H6("Counties"),
                        dcc.Graph(id='county_map'),

                    ]), color="primary", outline=True
                ), width=6, lg={'size':6 , 'offset':1 }, md={'size':10 , 'offset':1 }, xs={'size':12 , 'offset':0 }
            ),




#-----------------------------------------------------------------------------------------------------------------------

            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        dbc.Col(
                            html.H5("County Comparison:", className="card-title"), width={"size": 8, "offset": 3}
                        ),

                        dcc.Dropdown(
                            id='county_dropdown',
                            options=[
                                {'label':'Allegany', 'value':'Allegany'},{'label':'Anne Arundel', 'value':'Anne Arundel'},
                                {'label':'Baltimore', 'value':'Baltimore'},{'label':'Calvert', 'value':'Calvert'},
                                {'label': 'Caroline', 'value': 'Caroline'}, {'label': 'Carroll', 'value': 'Carroll'},
                                {'label': 'Cecil', 'value': 'Cecil'}, {'label': 'Charles', 'value': 'Charles'},
                                {'label': 'Dorchester', 'value': 'Dorchester'}, {'label': 'Frederick', 'value': 'Frederick'},
                                {'label': 'Garrett', 'value': 'Garrett'}, {'label': 'Harford', 'value': 'Harford'},
                                {'label': 'Howard', 'value': 'Howard'}, {'label': 'Kent', 'value': 'Kent'},
                                {'label': 'Montgomery', 'value': 'Montgomery'}, {'label': 'Prince George\'s', 'value': 'Prince George\'s'},
                                {'label': 'Queen Anne\'s', 'value': 'Queen Anne\'s'}, {'label': 'St.Mary\'s', 'value': 'St.Mary\'s'},
                                {'label': 'Somerset', 'value': 'Somerset'}, {'label': 'Talbot', 'value': 'Talbot'},
                                {'label': 'Washington', 'value': 'Washington'}, {'label': 'Wiscomico', 'value': 'Wiscomico'},
                                {'label': 'Worcester', 'value': 'Worcester'}, {'label': 'Baltimore City', 'value': 'Baltimore City'},
                            ],
                            #value='Baltimore City',
                            multi=True,
                            placeholder='Select Counties for Comparison:',
                        ),

                        html.Hr(),
                        html.H6("Counties"),
                        dcc.Graph(id='bar_graph')

                    ]), color="primary", outline=True
                ), width= 4, lg={'size':4 , 'offset':0 }, md={'size':10 , 'offset':1 }, xs={'size':12 , 'offset':0 }
            ),

        ],
    ),



    html.Div(id='display')


])


#====  1  ==================  1  ================CALLBACK 1================  1  ==========================  1  ========
@app.callback(
    Output('county_map','figure'),
    [Input('month_slider','value')])

def update_graph(month_chosen):
    #dff = df
    dff = df.loc[1193:1216,['Admin2', 'FIPS', 'Population', 'January Total', 'February Total', 'March Total',
                            'April Total', 'May Total', 'June Total', 'July Total']]

    if month_chosen == 1:
        month_chosen = 'January Total'

    elif month_chosen == 2:
        month_chosen = 'February Total'

    elif month_chosen == 3:
        month_chosen = 'March Total'

    elif month_chosen == 4:
        month_chosen = 'April Total'

    elif month_chosen == 5:
        month_chosen = 'May Total'

    elif month_chosen == 6:
        month_chosen = 'June Total'

    elif month_chosen == 7:
        month_chosen = 'July Total'

    #fips = dff['FIPS']
    #values = dff[month_chosen]

    fig = px.choropleth_mapbox(
        data_frame=dff, geojson=counties, color=month_chosen,
        hover_name='Admin2',
        hover_data={'FIPS':False,
            month_chosen:True,
            'Population':True},
        locations='FIPS',
        color_continuous_scale=colorscale,
        #range_color=(0, 12),
        #mapbox_style=map_style,
        zoom=6, center = {"lat": 38.9072, "lon": -77.0369},
        opacity=0.5,
        #width=850,
        #height=575
    )

    fig.update_layout(mapbox_style=map_style, mapbox_accesstoken=token, clickmode='select+event', dragmode="lasso",
                      margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor= "rgba(125, 125, 125,1)", legend= {'itemsizing': 'constant'},
                      coloraxis_colorbar=dict(title='#of Deaths', thicknessmode='pixels', thickness=10, lenmode='pixels',
                                              len=450, ticks='outside', ticksuffix='Deaths'))

    #print(month_chosen)
    return (fig)


#====  2  ==================  2  ================CALLBACK 2================  2  ==========================  2  ========
@app.callback(Output('display','children'),[Input('county_map','selectedData')])

def selectData(selectData):
    return str('Selecting points produces a nested dictionary: {}'.format(selectData))


#====  3  ==================  3  ================CALLBACK 3================  3  ==========================  3  ========
@app.callback(
    Output('bar_graph','figure'),
    [Input('county_map','selectedData'),
     Input('county_dropdown','value'),
     Input('month_slider','value')])

def update_bargraph(selectData, countyChosen_Dropdown, monthChosen_Slider):
    #dff = df
    dff = df.loc[1193:1216,['Admin2', 'FIPS', 'Population', 'January Total', 'February Total', 'March Total',
                            'April Total', 'May Total', 'June Total', 'July Total']]


    print(selectData)

    if monthChosen_Slider == 1:
        monthChosen_Slider = 'January Total'

    elif monthChosen_Slider == 2:
        monthChosen_Slider = 'February Total'

    elif monthChosen_Slider == 3:
        monthChosen_Slider = 'March Total'

    elif monthChosen_Slider == 4:
        monthChosen_Slider = 'April Total'

    elif monthChosen_Slider == 5:
        monthChosen_Slider = 'May Total'

    elif monthChosen_Slider == 6:
        monthChosen_Slider = 'June Total'

    elif monthChosen_Slider == 7:
        monthChosen_Slider = 'July Total'

    #print(monthChosen_Slider)



    filtList = []
    if selectData is None:
        print('Hello')

    else:
        for i in range(len(selectData['points'])):
            filtList.append(selectData['points'][i]['hovertext'])
    #print(filtList)

    selectData = filtList



    data = []

    if countyChosen_Dropdown is not None:
        #print(countyChosen_Dropdown)

        for countyChosen_Dropdown in countyChosen_Dropdown:

            population = go.Bar(
                x=dff[dff['Admin2'] == countyChosen_Dropdown]['Admin2'],
                y=dff[dff['Admin2'] == countyChosen_Dropdown]['Population'], name='Population')
            data.append(population)

            deaths = go.Bar(
                x=dff[dff['Admin2'] == countyChosen_Dropdown]['Admin2'],
                y=dff[dff['Admin2'] == countyChosen_Dropdown][monthChosen_Slider], name='Deaths')
            data.append(deaths)

    if selectData is not None:
        #print(countyChosen_Dropdown)

        for selectData in selectData:
            population = go.Bar(
                x=dff[dff['Admin2'] == selectData]['Admin2'],
                y=dff[dff['Admin2'] == selectData]['Population'], name='Population')
            data.append(population)

            deaths = go.Bar(
                x=dff[dff['Admin2'] == selectData]['Admin2'],
                y=dff[dff['Admin2'] == selectData][monthChosen_Slider], name='Deaths')
            data.append(deaths)


    #print(data)

    layout = go.Layout(paper_bgcolor= "rgba(0,0,0,0)", bargap=0.15)
    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(yaxis_type="log", showlegend=False, margin={"r":10,"t":10,"l":10,"b":10},
                      uniformtext_minsize=3, uniformtext_mode='hide', bargroupgap=0.01,
                      plot_bgcolor='rgba(125, 125, 125,1)', autosize=False)
    fig.update_xaxes(tickangle=45, tickfont=dict(family='Rockwell', color='rgba(255, 105, 167,1)', size=9))
    fig.update_yaxes(tickfont=dict(family='Rockwell', color='rgba(255, 105, 167,1)', size=10))

    return fig

#==============================================APP LAYOUT===============================================================
if __name__=="__main__":
    app.run_server(debug=True)
