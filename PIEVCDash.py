import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
from pymongo import MongoClient
import numpy as np
import plotly.graph_objects as go
from pyvis import network as net
import dash_cytoscape as cyto
import dash_auth

#-----------------------------------------------------------------------------------------------------------------------
# Import Data
client = MongoClient("mongodb+srv://moradim:UofGPIEVC@cluster0.ok7am.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
DataBase = client["PIEVC"]
## Infrastructure Classification
InfraClassification_db = DataBase.InfraClassification
## Project Team
ProjectTeam_db = DataBase.ProjectTeam
## Studies Overview
StudiesOverview_db = DataBase.StudiesOverview
## Risk Profile
RiskProfile_db = DataBase.RiskProfile
## ClimateDataInfras
ClimateDataInfras_db = DataBase.ClimateDataInfras
ClimateDataInfras_df = pd.DataFrame(list(ClimateDataInfras_db.find()))
## Province Boundaries
AB_boundary_db = DataBase.AB_boundary
BC1_boundary_db = DataBase.BC1_boundary
BC2_boundary_db = DataBase.BC2_boundary
MB_boundary_db = DataBase.MB_boundary
NB_boundary_db = DataBase.NB_boundary
NL_boundary_db = DataBase.NL_boundary
NS1_boundary_db = DataBase.NS1_boundary
NS2_boundary_db = DataBase.NS2_boundary
NU_boundary_db = DataBase.NU_boundary
NWT_boundary_db = DataBase.NWT_boundary
ON_boundary_db = DataBase.ON_boundary
PEI_boundary_db = DataBase.PEI_boundary
QC_boundary_db = DataBase.QC_boundary
SK_boundary_db = DataBase.SK_boundary
YT_boundary_db = DataBase.YT_boundary
## Province Boundaries
ClimateData_db = DataBase.ClimateData
ClimateData_df = pd.DataFrame(list(ClimateData_db.find()))
## Recommendation
Recommendation_db = DataBase.Recommendation
Recommendation_df = pd.DataFrame(list(Recommendation_db.find()))

#-----------------------------------------------------------------------------------------------------------------------
# Start App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

auth = dash_auth.BasicAuth(
    app,
    {'UofGPIEVC': 'Xj#%:(3:fYfRp(Mz'}
)

#-----------------------------------------------------------------------------------------------------------------------
# App Style
# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "20rem",
    "padding": "2rem 1rem",
    "background-color": "#DEFFD2",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "20rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    'display': 'flex'
}

sidebar = html.Div(
    [
        html.H1("PIEVC Reports Assessment", className="display-4"),
        html.Hr(),
        html.Label("This app reviews and evaluates the vulnerability of Canadian infrastructure to the anticipated effects of climate change. This is conducted through a review of a selection of PIEVC assessments published over the years 2016 to 2021."),
        html.Img(src=app.get_asset_url('Logo.png')),
    ],
    style=SIDEBAR_STYLE,
)

drop_opt = [{'label':study_id,'value':study_id} for study_id in pd.DataFrame(list(ProjectTeam_db.find()))['Study'].unique().tolist()]
drop_Study = dcc.Dropdown(id='drop_Study',clearable=False,searchable=False,options=drop_opt,value=drop_opt[0]['value'],style={'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'})
drop_province = dcc.Dropdown(id='drop_province',clearable=False,searchable=False,multi=True,style={'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'})
drop_study_multi = dcc.Dropdown(id='opt_infra_province_study',clearable=False,searchable=False,multi=True,style={'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'})
drop_study_threshold = dcc.Dropdown(id='opt_study_threshold',clearable=False,searchable=False,style={'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'})
drop_study_sunburstRisk1 = dcc.Dropdown(id='opt_study_sunburstRisk1',clearable=False,searchable=False,style={'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'})
drop_study_sunburstRisk2 = dcc.Dropdown(id='opt_study_sunburstRisk2',clearable=False,searchable=False,style={'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'})
drop_location_sunburstRisk1 = dcc.Dropdown(id='opt_location_sunburstRisk1',clearable=False,searchable=False,style={'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'})
drop_location_sunburstRisk2 = dcc.Dropdown(id='opt_location_sunburstRisk2',clearable=False,searchable=False,style={'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'})
drop_risklevel_sunburstRisk1 = dcc.Dropdown(id='opt_risklevel_sunburstRisk1',clearable=False,searchable=False,options=[{'label':'High','value':'High'},{'label':'Medium','value':'Medium'}], value='High', style={'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'})
drop_risklevel_sunburstRisk2 = dcc.Dropdown(id='opt_risklevel_sunburstRisk2',clearable=False,searchable=False,options=[{'label':'High','value':'High'},{'label':'Medium','value':'Medium'}], value='High',style={'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'})
drop_opt_timehorizon_sunburstRisk1 = [{'label':'Current','value':'Current'},{'label':'Short Term','value':'Short Term'},{'label':'Medium Term','value':'Medium Term'},{'label':'Long Term','value':'Long Term'}]
drop_timehorizon_sunburstRisk1 = dcc.Dropdown(id='opt_timehorizon_sunburstRisk1',clearable=False,searchable=False,options=drop_opt_timehorizon_sunburstRisk1, value=drop_opt_timehorizon_sunburstRisk1[0]['value'], style={'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'})
drop_timehorizon_sunburstRisk2 = dcc.Dropdown(id='opt_timehorizon_sunburstRisk2',clearable=False,searchable=False,options=drop_opt_timehorizon_sunburstRisk1, value=drop_opt_timehorizon_sunburstRisk1[0]['value'], style={'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'})

drop_opt_infra = [{'label':i,'value':i} for i in pd.DataFrame(list(InfraClassification_db.find()))['Infrastructure'].unique().tolist()]
drop_InfraClass_multi = dcc.Dropdown(id='drop_InfraClass_multi',clearable=False,searchable=False,options=drop_opt_infra,value='Buildings',multi=True,style={'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'})
drop_InfraClass_single = dcc.Dropdown(id='drop_InfraClass_single',clearable=False,searchable=False,options=drop_opt_infra,value='Buildings',style={'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'})

#-----------------------------------------------------------------------------------------------------------------------
# App Layout
app.layout = html.Div([
    sidebar,

    html.Div([
        html.Div([
            html.Div([
                html.H3('PIEVC Engineering Protocol'),
                html.Hr(),
                html.P('The PIEVC Protocol provides a structured, rigorous qualitative process to assess the risks and vulnerabilities of individual infrastructures or infrastructure systems to current and future extreme weather events and climate changes.')
            ],className='box',style={'margin-right': '-0.8rem','margin-left': '-1rem','margin-bottom': '1rem','margin-top': '1rem','padding-left':'15px','padding-right':'15px', 'padding-top':'15px', 'padding-bottom':'15px','backgroundColor':'#111111','border-radius': '15px','background-color': '#F2F2F2'}),
        # <Box 1>: Infrastructure classification sunburst & Description
        html.Div([
            html.Div([
                html.Div([
                    html.H3('Infrastructure Classification',style={'padding-left': '15px'}),
                    html.Hr(style={'margin-right': '6rem','margin-left': '0.8rem'}),
                    html.Label('Click on it to know more!', style={'font-size': '9px','padding-left': '15px'}),
                    dcc.Graph(id='fig_sunburst_InfraClass'),
                ],style={'width':'55%'}),
                html.Div([
                    html.Div([
                        html.H3('Description of Infrastructure'),
                        html.Hr(style={'margin-right': '2rem'}),
                        html.P('Choose Infrastructure:'),
                    ],style={'width':'100%'}),
                    html.Div([
                        drop_InfraClass_single
                    ],style={'width':'80%','margin-left': '-0.7rem'}),
                    html.Div([
                        html.Div(id='InfraClass_Description',style={'padding-right':'15px'})
                    ])
                ],style={'width':'45%'})
            ],className='row')
        ],className='box',style={'margin-right': '-0.8rem','margin-left': '-1rem','margin-bottom': '1rem','margin-top': '1rem','padding-left':'15px', 'padding-top':'15px', 'padding-bottom':'15px','backgroundColor':'#111111','border-radius': '15px','background-color': '#F2F2F2'}),
        # <Box 2>: Overview table
        html.Div([
            html.Div([
                html.H3('Overview Table'),
                html.Hr(style={'margin-right': '30rem'}),
                html.P('An overview of PIEVC studies from 2016 to 2021 is shown below.'),
                html.Label('Scroll down to know more!', style={'font-size': '9px', 'padding-left': '5px'}),
            ]),
            html.Div([
                dcc.Graph(id='table_Overview')
            ])
        ],className='box',style={'margin-right': '-0.8rem','margin-left': '-1rem','margin-bottom': '1rem','margin-top': '1rem','padding-right':'15px','padding-left':'15px', 'padding-top':'15px', 'padding-bottom':'15px','backgroundColor':'#111111','border-radius': '15px','background-color': '#F2F2F2'}),
        # <Box 3>: Project Team
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.H3('Project Team'),
                        html.Hr(style={'margin-right': '30rem'})
                    ]),
                    html.Div([
                        html.P('Choose Study:')
                    ]),
                    html.Div([
                        drop_Study
                    ],style={'width':'40%','margin-left': '-0.6rem','margin-bottom': '0.5rem','margin-top': '-0.3rem'}),
                    dcc.Graph(id='table_ProjectTeam')
                ],style={'width':'63%','margin-right': '1rem','margin-left': '0rem','margin-bottom': '1rem','margin-top': '1rem','padding-right':'15px','padding-left':'15px', 'padding-top':'15px', 'padding-bottom':'15px','backgroundColor':'#111111','border-radius': '15px','background-color': '#F2F2F2'}),
                html.Div([
                    html.Img(src=app.get_asset_url('PIEVCImg.png'),style={'width': '100%', 'position': 'relative', 'opacity': '80%','margin-top': '1rem'})
                ],style={'width':'31%'}),
            ],className='row'),
        ],className='box'),
        # <Box >: Climate Data Map
        html.Div([
            html.Div([
                html.H3("Geo-Spatial Distribution of PIEVC reports"),
                html.Hr(style={'margin-right': '30rem'}),
                html.P('The map shows spatial distribution of PIEVC studies based on the chosen infrastructure from the sidebar.')
            ]),
            html.Div([
                html.Iframe(src='assets/ClimateMap.html',width='100%',height='400')
            ])
        ],className='box',style={'margin-right': '0rem','margin-left': '-0.5rem','margin-bottom': '1rem','margin-top': '1rem','padding-right':'15px','padding-left':'15px', 'padding-top':'15px', 'padding-bottom':'15px','backgroundColor':'#111111','border-radius': '15px','background-color': '#F2F2F2'}),
        # <Box >: Select Infrastructure & Select Location & Select Study
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Infrastructure, Location, and Study:"),
                    html.Hr(style={'margin-right': '5rem'}),
                    html.P('The results from PIEVC reports can be investigated based on the chosen infrastructure, location, and study')
                ]),
                html.Div([
                    html.Div([
                        html.P('Infrastructure:')
                    ],style={'margin-bottom':'-1rem'}),
                    html.Div([
                        drop_InfraClass_multi
                    ])
                ]),
                html.Div([
                    html.Div([
                        html.P('Location:')
                    ],style={'margin-bottom':'-1rem'}),
                    html.Div([
                        drop_province
                    ])
                ]),
                html.Div([
                    html.Div([
                        html.P('Study:')
                    ],style={'margin-bottom':'-1rem'}),
                    html.Div([
                        drop_study_multi
                    ])
                ])
            ],className='box',style={'width':'40%','margin-right': '0rem','margin-left': '0.3rem','margin-bottom': '1rem','margin-top': '1rem','padding-right':'15px','padding-left':'15px', 'padding-top':'15px', 'padding-bottom':'15px','backgroundColor':'#111111','border-radius': '15px','background-color': '#F2F2F2'}),
            # <Box >: Threshold
            html.Div([
                html.Div([
                    html.H3('Threshold'),
                    html.Hr(style={'margin-right':'10rem'}),
                    html.P('Choose study to see the sources used to calculate climate threshold')
                ]),
                html.Div([
                    drop_study_threshold
                ],style={'width':'50%'}),
                html.Div(id='Threshold_statement')
            ],className='box',style={'width':'57%','margin-right': '0rem','margin-left': '1rem','margin-bottom': '1rem','margin-top': '1rem','padding-right':'15px','padding-left':'15px', 'padding-top':'15px', 'padding-bottom':'15px','backgroundColor':'#111111','border-radius': '15px','background-color': '#F2F2F2'}),
        ],className='row'),
        # <Box >: Network Plot
        html.Div([
            html.Div([
                html.H3('Climate Parameters'),
                html.Hr(style={'width':'30'}),
                html.P('The common climate parameters among studies, and the climate parameters affect the infrastructures are shown below:')
            ]),
            html.Div(
                cyto.Cytoscape(id='NetworkPlot',layout={'name': 'circle'},style={'width': '100%', 'height': '400px'},elements=[],minZoom=0.2,maxZoom=1)
            ),
        ],className='box',style={'margin-right': '0rem','margin-left': '-0.9rem','margin-bottom': '1rem','margin-top': '1rem','padding-right':'15px','padding-left':'15px', 'padding-top':'15px', 'padding-bottom':'15px','backgroundColor':'#111111','border-radius': '15px','background-color': '#F2F2F2'}),
        # <Box > Risk Profile
        html.Div([
            html.Div([
                html.Div([
                    html.H3('Risk Analysis 1'),
                    html.Hr(),
                    html.P('Choose study, location, risk level and time horizon to see the risk profile')
                ]),
                html.Div([
                    html.Div([
                       html.P('Study:')
                    ],style={'margin-bottom':'-1rem'}),
                    html.Div([
                        drop_study_sunburstRisk1
                    ])
                ]),
                html.Div([
                    html.Div([
                        html.P('Location:')
                    ],style={'margin-bottom':'-1rem'}),
                    html.Div([
                        drop_location_sunburstRisk1
                        ])
                ]),
                html.Div([
                    html.Div([
                        html.P('Risk Level:')
                    ],style={'margin-bottom':'-1rem'}),
                    html.Div([
                        drop_risklevel_sunburstRisk1
                        ])
                ]),
                html.Div([
                    html.Div([
                       html.P('Time Horizon:')
                    ], style={'margin-bottom': '-1rem'}),
                    html.Div([
                        drop_timehorizon_sunburstRisk1
                        ])
                ]),
                html.Div([
                    dcc.Graph(id='Risk_sunburst1')
                ])
            ],className='box',style={'width':'49%','margin-right': '0rem','margin-left': '0rem','margin-bottom': '1rem','margin-top': '1rem','padding-right':'15px','padding-left':'15px', 'padding-top':'15px', 'padding-bottom':'15px','backgroundColor':'#111111','border-radius': '15px','background-color': '#F2F2F2'}),
            html.Div([
                html.Div([
                    html.H3('Risk Analysis 2'),
                    html.Hr(),
                    html.P('Choose study, location, risk level and time horizon to see the risk profile')
                ]),
                html.Div([
                    html.Div([
                        html.P('Study:')
                    ], style={'margin-bottom': '-1rem'}),
                    html.Div([
                        drop_study_sunburstRisk2
                    ])
                ]),
                html.Div([
                    html.Div([
                        html.P('Location:')
                    ], style={'margin-bottom': '-1rem'}),
                    html.Div([
                        drop_location_sunburstRisk2
                    ])
                ]),
                html.Div([
                    html.Div([
                        html.P('Risk Level:')
                    ], style={'margin-bottom': '-1rem'}),
                    html.Div([
                        drop_risklevel_sunburstRisk2
                    ])
                ]),
                html.Div([
                    html.Div([
                        html.P('Time Horizon:')
                    ], style={'margin-bottom': '-1rem'}),
                    html.Div([
                        drop_timehorizon_sunburstRisk2
                    ])
                ]),
                html.Div([
                    dcc.Graph(id='Risk_sunburst2')
                ])
            ],className='box',style={'width':'49%','margin-right': '0rem','margin-left': '1rem','margin-bottom': '1rem','margin-top': '1rem','padding-right':'15px','padding-left':'15px', 'padding-top':'15px', 'padding-bottom':'15px','backgroundColor':'#111111','border-radius': '15px','background-color': '#F2F2F2'})
        ],className='row'),
        html.Div([
            html.Div([
                html.H3('Recommendations'),
                html.Hr()
            ]),
            html.Div(id='Recom_statement')
        ],className='box',style={'margin-right': '-0.5rem','margin-left': '-0.8rem','margin-bottom': '1rem','margin-top': '1rem','padding-right':'15px','padding-left':'15px', 'padding-top':'15px', 'padding-bottom':'15px','backgroundColor':'#111111','border-radius': '15px','background-color': '#F2F2F2'})

    ],className='main',style={"margin-left": "22rem","margin-right": "2rem"}),
    ])
])

#-----------------------------------------------------------------------------------------------------------------------
@app.callback(
    [Output('InfraClass_Description','children'),
     Output('fig_sunburst_InfraClass','figure')],
    [Input("drop_InfraClass_single", "value")]
)
def InfraClassification(opt_infra):

    InfraClassification_df = pd.DataFrame(list(InfraClassification_db.find()))
    InfraClassification_df.replace(to_replace="NAN", value=np.nan, inplace=True)
    title = "SunBurst Plot Infrastructure Classification"

    # Infrastructure classification sunburst plot
    sb = px.sunburst(InfraClassification_df, path=['Infrastructure', 'Infrastructure Component 1', 'Infrastructure Component 2'],custom_data=['Infrastructure', 'Infrastructure Component 1'])
    sb.update_layout(margin={'l': 0, 'r': 0, 'b': 0, 't': 0},paper_bgcolor='rgba(0,0,0,0)') # , width=1000, height=1000
    sb.update_traces(hovertemplate='<b>Infrastructure Type: %{customdata[0]} <br> Label: %{label}',branchvalues='total', selector=dict(type='sunburst'))
    sb.update_traces(insidetextorientation='radial', selector=dict(type='sunburst'))

    # Description
    InfraClassification_df = pd.DataFrame(list(InfraClassification_db.find()))
    descrip_statement = ''
    infra_desc_study = InfraClassification_df[InfraClassification_df['Infrastructure']==opt_infra]
    for i_infra_comp1 in infra_desc_study['Infrastructure Component 1'].unique().tolist():
        statement_ = ''
        for i_infra_descrip in infra_desc_study[infra_desc_study['Infrastructure Component 1']==i_infra_comp1]['Description']:
            if not i_infra_descrip == 'NAN':
                statement_ += '''* {} \n'''.format(i_infra_descrip)
        descrip_statement += '''###### {} \n'''.format(i_infra_comp1) + statement_

    return html.Div([dcc.Markdown(descrip_statement)]),sb



@app.callback([Output('table_Overview','figure'),
               Output('table_ProjectTeam','figure')],
              [Input('drop_Study','value')]
)
def Overview_Team_Table(opt_study):

    # Overview Table
    StudiesOverview_df = pd.DataFrame(list(StudiesOverview_db.find()))
    StudiesOverview_df = StudiesOverview_df.drop(columns=['_id'])
    table_Overview = go.Figure(data=[go.Table(
        columnwidth=[400, 200, 250, 200, 120, 300, 100],
        header=dict(values=list(StudiesOverview_df.columns),
                    fill_color='grey',
                    line_color='darkslategray',
                    align=['center', 'center', 'center', 'center', 'center', 'center', 'center'],
                    font=dict(color='white', size=12)),
        cells=dict(values=[StudiesOverview_df.Title, StudiesOverview_df['Consultant Company'], StudiesOverview_df['Client'],
                           StudiesOverview_df.Location, StudiesOverview_df.Year,
                           StudiesOverview_df['Infrastructure'], StudiesOverview_df['Site Visit']],
                   fill_color='white',
                   align=['left', 'center', 'center', 'center', 'center', 'center', 'center'],
                   line_color='darkslategray'))
    ])
    table_Overview.update_layout(margin={'l': 0, 'r': 0, 'b': 0, 't': 0})

    # Project Team
    ProjectTeam_df = pd.DataFrame(list(ProjectTeam_db.find()))
    ProjectTeam_opt = ProjectTeam_df.loc[ProjectTeam_df.Study == opt_study]
    ProjectTeam_opt = ProjectTeam_opt.drop(columns=['Study'])
    ProjectTeam_opt = ProjectTeam_opt.drop(columns=['_id'])
    table_ProjectTeam = go.Figure(data=[go.Table(
        columnwidth=[250, 300, 250],
        header=dict(values=list(ProjectTeam_opt.columns),
                    fill_color='grey',
                    line_color='darkslategray',
                    align=['center', 'center', 'center'],
                    font=dict(color='white', size=12)),
        cells=dict(values=[ProjectTeam_opt['Team Member'], ProjectTeam_opt['Role'], ProjectTeam_opt['Organization']],
                   fill_color='white',
                   align=['center', 'center', 'center'],
                   line_color='darkslategray'))
    ])
    table_ProjectTeam.update_layout(margin={'l': 0, 'r': 0, 'b': 0, 't': 0})
    table_ProjectTeam.update_layout(height=250)

    return table_Overview,table_ProjectTeam

@app.callback([Output('drop_province','options'),
               Output('drop_province','value')],
              [Input('drop_InfraClass_multi','value')]
)
def Select_Infrastructure_Province(opt_infra_multi):

    RiskProfile_df = pd.DataFrame(list(RiskProfile_db.find()))

    # Extract provinces with the given infrastructures
    if isinstance(opt_infra_multi, list):
        opt_infra_multi_list = opt_infra_multi
    else:
        opt_infra_multi_list = [opt_infra_multi]

    opt_provinces = RiskProfile_df[RiskProfile_df['Infrastructure'].isin(opt_infra_multi_list)]['Province'].unique().tolist()
    opt_provinces = [dict(label=val, value=val) for val in opt_provinces]

    return opt_provinces,opt_provinces[0]['value']


@app.callback([Output('opt_infra_province_study','options'),
               Output('opt_infra_province_study','value')],
              [Input('drop_InfraClass_multi','value'),
               Input('drop_province','value')]
)
def Select_Study(opt_infra_multi,opt_province_multi):
    RiskProfile_df = pd.DataFrame(list(RiskProfile_db.find()))

    # Extract study with the given infrastructures and provinces
    if isinstance(opt_infra_multi, list):
        opt_infra_multi_list = opt_infra_multi
    else:
        opt_infra_multi_list = [opt_infra_multi]

    provinces_df = RiskProfile_df[RiskProfile_df['Infrastructure'].isin(opt_infra_multi_list)]

    if isinstance(opt_province_multi, list):
        opt_province_multi_list = opt_province_multi
    else:
        opt_province_multi_list = [opt_province_multi]

    opt_infra_province_study_list = provinces_df[provinces_df['Province'].isin(opt_province_multi_list)]['Study'].unique().tolist()
    opt_infra_province_study = [dict(label=val, value=val) for val in opt_infra_province_study_list]

    return opt_infra_province_study,opt_infra_province_study[0]['value']


@app.callback([Output('opt_study_threshold','options'),
               Output('opt_study_threshold','value')],
              [Input('drop_InfraClass_multi','value'),
               Input('drop_province','value')]
)
def Select_Study_Threshold(opt_infra_multi,opt_province_multi):
    RiskProfile_df = pd.DataFrame(list(RiskProfile_db.find()))

    # Extract study with the given infrastructures and provinces
    if isinstance(opt_infra_multi, list):
        opt_infra_multi_list = opt_infra_multi
    else:
        opt_infra_multi_list = [opt_infra_multi]

    provinces_df = RiskProfile_df[RiskProfile_df['Infrastructure'].isin(opt_infra_multi_list)]

    if isinstance(opt_province_multi, list):
        opt_province_multi_list = opt_province_multi
    else:
        opt_province_multi_list = [opt_province_multi]

    opt_infra_province_study_list = provinces_df[provinces_df['Province'].isin(opt_province_multi_list)]['Study'].unique().tolist()
    opt_infra_province_study = [dict(label=val, value=val) for val in opt_infra_province_study_list]

    return opt_infra_province_study,opt_infra_province_study[0]['value']


@app.callback(Output('Threshold_statement','children'),
              [Input('opt_study_threshold','value')]
)
def Threshold_Description(opt_study_thres):

    Threshold_statement_list = ClimateData_df[ClimateData_df['Study']==opt_study_thres]['Threshold'].values.tolist()[0].split('&&')
    Statement_out = ''
    for Thr_st in Threshold_statement_list:
        title_st, statement_st = Thr_st.split(':')
        Statement_out += '''** {} :** \n {} \n'''.format(title_st,statement_st)

    return html.Div([dcc.Markdown(Statement_out)])


@app.callback(Output('NetworkPlot','elements'),
              [Input('opt_infra_province_study','value'),
               Input('drop_InfraClass_multi','value')]
)
def NetworkPlot(opt_infra_province_study,drop_InfraClass_multi):
    RiskProfile_df = pd.DataFrame(list(RiskProfile_db.find()))

    if isinstance(opt_infra_province_study, list):
        opt_infra_province_study_list = opt_infra_province_study
    else:
        opt_infra_province_study_list = [opt_infra_province_study]

    if isinstance(drop_InfraClass_multi, list):
        drop_InfraClass_multi_list = drop_InfraClass_multi
    else:
        drop_InfraClass_multi_list = [drop_InfraClass_multi]

    ClimateParam_list = []
    for i_study in opt_infra_province_study_list:
        list_infras = RiskProfile_df['Infrastructure'][RiskProfile_df['Study'] == i_study].unique().tolist()
        list_infras_study = list(set(list_infras).intersection(set(drop_InfraClass_multi_list)))
        for i_infra in list_infras_study:
            list_infras_study_clim = ClimateDataInfras_df['ClimateParam'][(ClimateDataInfras_df[i_infra] == 'Yes') & (ClimateDataInfras_df['Study'] == i_study)].unique().tolist()

            ClimateParam_list += list_infras_study_clim
    ClimateParam_list = list(set(ClimateParam_list))

    ClimateParam_nodes = []
    for i_elm in ClimateParam_list:
        ClimateParam_nodes.append({'data':{'id':i_elm,'label':i_elm}})

    Infras_nodes = []
    for i_study in opt_infra_province_study_list:
        list_infras = RiskProfile_df['Infrastructure'][RiskProfile_df['Study'] == i_study].unique().tolist()
        list_infras_study = list(set(list_infras).intersection(set(drop_InfraClass_multi_list)))
        for i_infras_study in list_infras_study:
            Infras_nodes.append({'data':{'id':i_study+i_infras_study, 'label':i_study+i_infras_study}})

    edges = []
    for i_study in opt_infra_province_study_list:
        list_infras = RiskProfile_df['Infrastructure'][RiskProfile_df['Study'] == i_study].unique().tolist()
        list_infras_study = list(set(list_infras).intersection(set(drop_InfraClass_multi_list)))
        for i_infra in list_infras_study:
            list_infras_study_clim = ClimateDataInfras_df['ClimateParam'][(ClimateDataInfras_df[i_infra] == 'Yes') & (ClimateDataInfras_df['Study'] == i_study)].unique().tolist()
            for mm in list_infras_study_clim:
                edges.append({'data':{'source':i_study+i_infra,'target':mm}})

    my_elements = Infras_nodes + ClimateParam_nodes + edges

    return my_elements


@app.callback([Output('opt_study_sunburstRisk1','options'),
               Output('opt_study_sunburstRisk1','value')],
              [Input('opt_infra_province_study','options')]
)
def Select_Study_SunburstRisk1(opt_infra_province_study):

    opt_study_sunburstRisk1 = opt_infra_province_study

    return opt_study_sunburstRisk1, opt_study_sunburstRisk1[0]['value']


@app.callback([Output('opt_location_sunburstRisk1','options'),
               Output('opt_location_sunburstRisk1','value')],
              [Input('opt_study_sunburstRisk1','value')]
)
def Select_Location_SunburstRisk1(opt_study_sunburstRisk1):
    RiskProfile_df = pd.DataFrame(list(RiskProfile_db.find()))

    Location_list = RiskProfile_df['Location'][RiskProfile_df['Study'] == opt_study_sunburstRisk1].unique().tolist()
    opt_location_sunburstRisk1 = [dict(label=val, value=val) for val in Location_list]

    return opt_location_sunburstRisk1, opt_location_sunburstRisk1[0]['value']


@app.callback([Output('opt_study_sunburstRisk2','options'),
               Output('opt_study_sunburstRisk2','value')],
              [Input('opt_infra_province_study','options')]
)
def Select_Study_SunburstRisk2(opt_infra_province_study):

    opt_study_sunburstRisk2 = opt_infra_province_study

    return opt_study_sunburstRisk2, opt_study_sunburstRisk2[0]['value']


@app.callback([Output('opt_location_sunburstRisk2','options'),
               Output('opt_location_sunburstRisk2','value')],
              [Input('opt_study_sunburstRisk2','value')]
)
def Select_Location_SunburstRisk2(opt_study_sunburstRisk2):
    RiskProfile_df = pd.DataFrame(list(RiskProfile_db.find()))
    Location_list = RiskProfile_df['Location'][RiskProfile_df['Study'] == opt_study_sunburstRisk2].unique().tolist()
    opt_location_sunburstRisk2 = [dict(label=val, value=val) for val in Location_list]

    return opt_location_sunburstRisk2, opt_location_sunburstRisk2[0]['value']


@app.callback([Output('Risk_sunburst1','figure'),
               Output('Risk_sunburst2','figure')],
              [Input('opt_study_sunburstRisk1','value'),
               Input('opt_location_sunburstRisk1','value'),
               Input('opt_risklevel_sunburstRisk1','value'),
               Input('opt_timehorizon_sunburstRisk1','value'),
               Input('opt_study_sunburstRisk2','value'),
               Input('opt_location_sunburstRisk2','value'),
               Input('opt_risklevel_sunburstRisk2','value'),
               Input('opt_timehorizon_sunburstRisk2','value'),
               Input('drop_InfraClass_multi','value')]
)
def RiskProf_Plot(opt_study_sunburstRisk1,opt_location_sunburstRisk1,opt_risklevel_sunburstRisk1,opt_timehorizon_sunburstRisk1,
                  opt_study_sunburstRisk2,opt_location_sunburstRisk2,opt_risklevel_sunburstRisk2,opt_timehorizon_sunburstRisk2,
                  drop_InfraClass_multi):

    def RiskScoreValueCalculator(var):
        if var == 'High':
            score = 10
        elif var == 'Med' or var == 'Mod-Low' or var == 'Mod-High':
            score = 5
        elif var == 'Low':
            score = 0
        else:
            score = 0
        return score

    if isinstance(drop_InfraClass_multi, list):
        drop_InfraClass_multi_list = drop_InfraClass_multi
    else:
        drop_InfraClass_multi_list = [drop_InfraClass_multi]

    # Plot 1
    RiskProfile_df = pd.DataFrame(list(RiskProfile_db.find()))
    Risk_timehorizon1 = 'Risk '+'('+opt_timehorizon_sunburstRisk1+')'
    RiskProfile_df['Score1'] = RiskProfile_df[Risk_timehorizon1].apply(RiskScoreValueCalculator)
    # print(opt_location_sunburstRisk1)
    df_sb_col1 = RiskProfile_df[(RiskProfile_df['Study'] == opt_study_sunburstRisk1) & (RiskProfile_df['Location'] == opt_location_sunburstRisk1)]
    df_sb_col1 = df_sb_col1[df_sb_col1['Infrastructure'].isin(drop_InfraClass_multi_list)]
    if opt_risklevel_sunburstRisk1 == 'High':
        path = ['Infrastructure', 'Climate Parameter']
    else:
        path = ['Infrastructure', 'Infrastructure Component 1', 'Climate Parameter']

    sb1 = px.sunburst(df_sb_col1, path=path, color='Score1', color_continuous_scale='hot_r', range_color=(0, 10),custom_data=[Risk_timehorizon1, 'Infrastructure', 'Score1'])
    sb1.update_coloraxes(colorbar=dict(tickmode="array", tickvals=[0, 5, 10], ticktext=['Low', 'Moderate', 'High']))
    sb1.update_layout(coloraxis_colorbar_title='Risk')
    sb1.update_layout(margin={'l': 0, 'r': 0, 'b': 0, 't': 0})
    sb1.update_traces(hovertemplate='<b>Infrastructure Type: %{customdata[1]} <br> Label: %{label}',branchvalues='total', selector=dict(type='sunburst'))
    sb1.update_traces(insidetextorientation='radial', selector=dict(type='sunburst'))

    # Plot 2
    Risk_timehorizon2 = 'Risk '+'('+opt_timehorizon_sunburstRisk2+')'
    RiskProfile_df['Score2'] = RiskProfile_df[Risk_timehorizon2].apply(RiskScoreValueCalculator)

    df_sb_col2 = RiskProfile_df[(RiskProfile_df['Study'] == opt_study_sunburstRisk2) & (RiskProfile_df['Location'] == opt_location_sunburstRisk2)]
    df_sb_col2 = df_sb_col2[df_sb_col2['Infrastructure'].isin(drop_InfraClass_multi_list)]
    if opt_risklevel_sunburstRisk2 == 'High':
        path = ['Infrastructure', 'Climate Parameter']
    else:
        path = ['Infrastructure', 'Infrastructure Component 1', 'Climate Parameter']

    sb2 = px.sunburst(df_sb_col2, path=path, color='Score2', color_continuous_scale='hot_r', range_color=(0, 10),custom_data=[Risk_timehorizon2, 'Infrastructure', 'Score2'])
    sb2.update_coloraxes(colorbar=dict(tickmode="array", tickvals=[0, 5, 10], ticktext=['Low', 'Moderate', 'High']))
    sb2.update_layout(coloraxis_colorbar_title='Risk')
    sb2.update_layout(margin={'l': 0, 'r': 0, 'b': 0, 't': 0})
    sb2.update_traces(hovertemplate='<b>Infrastructure Type: %{customdata[1]} <br> Label: %{label}',branchvalues='total', selector=dict(type='sunburst'))
    sb2.update_traces(insidetextorientation='radial', selector=dict(type='sunburst'))

    return sb1, sb2

@app.callback(Output('Recom_statement','children'),
              [Input('opt_infra_province_study','value')]
)
def Recommendation_Statement(opt_infra_province_study):

    if isinstance(opt_infra_province_study, list):
        opt_infra_province_study_list = opt_infra_province_study
    else:
        opt_infra_province_study_list = [opt_infra_province_study]

    df_st = Recommendation_df[Recommendation_df['Study'].isin(opt_infra_province_study_list)]

    Statement_out = ''
    for i_study in df_st['Study'].unique().tolist():
        Infras = df_st['Infrastructure'][df_st['Study']==i_study].unique().tolist()
        Statement_out += '''## {} \n'''.format(i_study)
        for i_infras in Infras:
            Statement_out += '''\n** {} :**\n'''.format(i_infras)
            Recoms = df_st['Recommendation'][(df_st['Study']==i_study) & (df_st['Infrastructure']==i_infras)].tolist()
            for i_recom in Recoms:
                Statement_out += '''* {} \n'''.format(i_recom)

    return html.Div([dcc.Markdown(Statement_out)])

if __name__ == '__main__':
    app.run_server(debug=True, port=3000)
