import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import dash_table
from dash.dependencies import Input, Output, State
import pickle
import numpy as np


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

loadIBM = pickle.load(open('pickle_IBM_dashboard_dummies.csv','rb'))
loadIBM_predict= pickle.load(open('pickle_IBM_dummies_new.csv','rb'))
loadIBM_predict.drop(['Attrition'],axis = 1, inplace =True)

app.layout = html.Div(children = [
    html.Img(src = '/assets/IBM.png', height = '100px'),
    html.Center(html.H1('IBM HR PREDICTION')),
    html.Center(html.H3('Employee Attrition')),
    html.P('Created by: Widya'),
    ##tabs
    dcc.Tabs(value = 'tabs', id = 'tabs-1', children = [
        dcc.Tab(label = 'Datatable', value = 'tab-nol', children = [
            html.Center(html.H1('DATA FRAME IBM ATTRITION')),
            html.Div(children = [
                html.P('Job Level : '),
                dcc.Dropdown(id = 'dropdown-joblevel', 
                            options =[{'label': 'All','value' :'All'}]+[{'label': i,'value' : i} for i in loadIBM['JobLevel'].unique()],
                            value = 'All')
            ],className = 'col-4'),
            
            html.Div(children = [
                html.P('Max Rows : '),
                dcc.Input(id = 'max-rows', type = 'number', value = 10)
            ],className = 'col-4'),

            html.Div(children = [
                html.Button('Search',id='search_joblevel')
            ], className = 'col-4',style = {'padding-top' : '10px', 'padding-bottom' : '10px'}),

            html.Div(id ='tampilan-datatable',
                    children =[
                    dash_table.DataTable(
                        id = 'Table',
                        columns = [{'name' : i, 'id' : i} for i in loadIBM.columns],
                        data = loadIBM.to_dict('records'),
                        page_action = 'native',
                        style_table={'overflowX': 'scroll'},
                        sort_action='native',
                        filter_action='native',
                        style_cell={
                            'height': 'auto',
                            'minWidth': '0px', 'maxWidth': '180px',
                            'whiteSpace': 'normal'
                        },
                        page_current = 0,
                        page_size = 10,
                    )]
            ),
        ]),

        #Top Navigation Bar Feature Selection
        dcc.Tab(label = 'Feature Selection', value = 'tab-dua', children =[
            html.Div(children = [
            html.Div(children = [
                dcc.Markdown('''
                ### Feature Importances ###
                '''
                ),
            html.Img(src = '/assets/Feature_Importance.jpg', height = '750px')  
            ], className = 'col-8'),
            #Permutation
            html.Div(children = [
                dcc.Markdown('''
                ### Permutation Importances ###
                '''
                ),
            html.Img(src = '/assets/Permutation.png', height = '600px') 
            ], className = 'col-3'),
            ] , className = 'row'
            ) 
        ]),
            

        dcc.Tab(label = 'Attrition Prediction', children = [
            html.Div(children=[
                html.Div(children = [
                    html.P('Age'),
                    dcc.Input(id = 'predict_age', type = 'number',placeholder = 'Input number of your age',style = {'width': '250px'})
                ],className = 'col-4'),
                html.Div(children = [
                    html.P('Distance From Home (miles)'),
                    dcc.Input(id = 'predict_distancefromhome', type = 'number',style = {'width': '250px'})
                ],className = 'col-4'),
                html.Div(children = [
                    html.P('Education'),
                    dcc.Dropdown(id = 'dropdown-education', 
                                options =[{'label': 'Below College','value' : 1},
                                          {'label': 'College','value' : 2},
                                          {'label': 'Bachelor','value' : 3},
                                          {'label': 'Master','value' : 4} ,
                                          {'label': 'Doctor','value' : 5}],
                                value =" ")
                ],className = 'col-3'),
                html.Div(children = [
                    html.P('Environment Satisfaction'),
                    dcc.Dropdown(id= 'dropdown-environmentsatisfaction',
                                options = [{'label': 'Low', 'value':1},
                                           {'label': 'Medium', 'value':2},
                                           {'label': 'High', 'value':3},
                                           {'label': 'Very High', 'value':4}],
                                value =" ")
                ],className = 'col-3', style = {'padding-top' : '50px'}),
                html.Div(children = [
                    html.P('Job Involvement'),
                    dcc.Dropdown(id='dropdown-jobinvolvement',
                                options = [{'label': 'Low', 'value':1},
                                           {'label': 'Medium', 'value':2},
                                           {'label': 'High', 'value':3},
                                           {'label': 'Very High', 'value':4}],
                                value =" ")
                ],className = 'col-3 offset-1', style = {'padding-top' : '50px'}),
                html.Div(children = [
                    html.P('Job Level'),
                    dcc.Dropdown(id='dropdown-predict_joblevel',
                                options = [{'label': 'General Staff', 'value':1},
                                           {'label': 'Supervisor', 'value':2},
                                           {'label': 'Junior Manager', 'value':3},
                                           {'label': 'Senior Manager', 'value':4},
                                           {'label': 'Executive','value':5}],
                                value =" ")
                ],className = 'col-3 offset-1', style = {'padding-top' : '50px'}),
                html.Div(children = [
                    html.P('Job Satisfaction'),
                    dcc.Dropdown(id='dropdown-jobsatisfaction',
                                options = [{'label': 'Low', 'value':1},
                                           {'label': 'Medium', 'value':2},
                                           {'label': 'High', 'value':3},
                                           {'label': 'Very High', 'value':4}],
                                value =" ")
                ],className = 'col-3', style = {'padding-top' : '50px'}),
                html.Div(children = [
                    html.P('Monthly Income($)'),
                    dcc.Input(id = 'predict_monthlyincome', type = 'number',placeholder = 'Input your month salary',style = {'width': '250px'})
                ],className = 'col-4 offset-1', style = {'padding-top' : '50px'}),
                html.Div(children= [
                    html.P('Relationship Satisfaction'),
                    dcc.Dropdown(id='dropdown-relationshipsatisfaction',
                                options = [{'label': 'Low', 'value':1},
                                           {'label': 'Medium', 'value':2},
                                           {'label': 'High', 'value':3},
                                           {'label': 'Very High', 'value':4}],
                                value =" ")
                ],className = 'col-3', style = {'padding-top' : '50px'}),
                html.Div(children = [
                    html.P('Stock Option Level'),
                    dcc.Dropdown(id='dropdown-stockoptionlevel',
                                options = [{'label': 'None', 'value':0},
                                           {'label': 'Low', 'value':1},
                                           {'label': 'Medium', 'value':2},
                                           {'label': 'High', 'value':3}],
                                value =" ")
                ],className = 'col-3',style = {'padding-top' : '50px'}),
                html.Div(children =[
                    html.P('Total Working Years'),
                    dcc.Input(id = 'predict_totalworkingyears', type = 'number',placeholder = 'Input your total working years',style = {'width': '250px'})
                ],className = 'col-3 offset-1', style = {'padding-top' : '50px'}),
                html.Div(children = [
                    html.P('Training Times Last Year'),
                    dcc.Input(id = 'predict_trainingtimeslastyear', type = 'number',placeholder = 'Input your training times last year',style = {'width': '250px'})
                ],className = 'col-3 offset-1', style = {'padding-top' : '50px'}),
                html.Div(children = [
                    html.P('Years at Company'),
                    dcc.Input(id = 'predict_yearsatcompany', type = 'number',placeholder = 'Input total years at IBM',style = {'width': '250px'})
                ],className = 'col-3', style = {'padding-top' : '50px'}),
                html.Div(children = [
                    html.P('Years in Current Role'),
                    dcc.Input(id = 'predict_yearsincurrentrole', type = 'number',placeholder = 'Input total years in current role',style = {'width': '250px'})
                ],className = 'col-3 offset-1', style = {'padding-top' : '50px'}),
                html.Div(children = [
                    html.P('Years with Current Manager'),
                    dcc.Input(id = 'predict_yearswithcurrentmanager', type = 'number',placeholder = 'Input total years with your current manager',style = {'width': '320px'})
                ],className = 'col-3 offset-1', style = {'padding-top' : '50px'}),
                html.Div(children =[
                    html.P('Gender'),
                    dcc.Dropdown(id='dropdown-gender',
                                options = [{'label': 'Female', 'value':0},
                                           {'label': 'Male', 'value':1}],
                                value =" ")
                ],className = 'col-3',style = {'padding-top' : '50px'}),
                html.Div(children =[
                    html.P('Marital Status'),
                    dcc.Dropdown(id='dropdown-maritalstatus',
                                options = [{'label': 'No Single (Married / Divorce)', 'value':0},
                                           {'label': 'Single', 'value':1}],
                                value =" ")
                ],className = 'col-3 offset-1',style = {'padding-top' : '50px'}),
                html.Div(children = [
                    html.P('Overtime'),
                    dcc.Dropdown(id='dropdown-overtime',
                                options = [{'label': 'No', 'value':0},
                                           {'label': 'Yes', 'value':1}],
                                value =" ")
                ],className = 'col-3 offset-1',style = {'padding-top' : '50px'}),
        ], className = 'row'),
        html.Div(html.Button('Search',id = 'search_attrition_predict'),
        className = 'col-4',style = {'padding-top' : '10px', 'padding-bottom' : '10px'}
        ),
        html.Div(id = 'result_attrition', children = 
            html.Center(html.H1('Please fill all the value'))
        )

        ]),

    ],
        # Tabs Content Style
    content_style = {
        'fontFamily' : 'Arial',
        'borderBottom' : '2px solid #d6d6d6',
        'borderLeft' : '2px solid #d6d6d6',
        'borderRight' : '2px solid #d6d6d6',
        'padding' : '44px'
    }
    )
],
style = {
    'maxWidth' : '1200px',
    'margin' : '0 auto',
})

    

@app.callback(
    Output(component_id='tampilan-datatable' , component_property='children'),
    [Input(component_id ='search_joblevel', component_property='n_clicks')],
    [State(component_id='dropdown-joblevel', component_property='value'),
    State(component_id ='max-rows',component_property= 'value')]
)
def update_output(n_clicks, joblevel, size):
    if joblevel=='All':
        children = [dash_table.DataTable(id='table',
            columns=[{"name": i, 'id' : i} for i in loadIBM.columns],
            data=loadIBM.to_dict('records'),
            page_action = 'native',
            page_current = 0,
            style_table={'overflowX': 'scroll'},
            sort_action='native',
            filter_action='native',
            page_size = size)]
    else:
        children = [dash_table.DataTable(id='table',
            columns=[{"name": i, 'id' : i} for i in loadIBM.columns],
            data=loadIBM[loadIBM['JobLevel']==joblevel].to_dict('records'),
            page_action = 'native',
            page_current = 0,
            style_table={'overflowX': 'scroll'},
            sort_action='native',
            filter_action='native',
            page_size = size)]
    return children

@app.callback(
    Output(component_id='result_attrition', component_property='children'),
    [Input(component_id='search_attrition_predict', component_property='n_clicks')],
    [State(component_id='predict_age', component_property='value'),
    State(component_id='predict_distancefromhome', component_property='value'),
    State(component_id='dropdown-education', component_property='value'),
    State(component_id='dropdown-environmentsatisfaction', component_property='value'),
    State(component_id='dropdown-jobinvolvement', component_property='value'),
    State(component_id='dropdown-predict_joblevel', component_property='value'),
    State(component_id='dropdown-jobsatisfaction', component_property='value'),
    State(component_id='predict_monthlyincome', component_property='value'),
    State(component_id='dropdown-relationshipsatisfaction', component_property='value'),
    State(component_id='dropdown-stockoptionlevel', component_property='value'),
    State(component_id='predict_totalworkingyears', component_property='value'),
    State(component_id='predict_trainingtimeslastyear', component_property='value'),
    State(component_id='predict_yearsatcompany', component_property='value'),
    State(component_id='predict_yearsincurrentrole', component_property='value'),
    State(component_id='predict_yearswithcurrentmanager', component_property='value'),
    State(component_id='dropdown-gender', component_property='value'),
    State(component_id='dropdown-maritalstatus', component_property='value'),
    State(component_id='dropdown-overtime', component_property='value')]
)


def check_attrition(n_clicks,Input_feat1,Input_feat2, Input_feat3, Input_feat4,Input_feat5,Input_feat6,Input_feat7,Input_feat8,Input_feat9,Input_feat10,Input_feat11,Input_feat12,Input_feat13,Input_feat14,Input_feat15,Input_feat16,Input_feat17,Input_feat18):
    if n_clicks ==None:
        return 'Please input all features'
    else:
        loadModel = pickle.load(open('pickle_Random_Forest_os_best_accuracy.sav','rb'))
        loadScaler = pickle.load(open('pickle_Standard_Scaler.sav','rb'))
        to_predict=np.array([Input_feat1,Input_feat2, Input_feat3, Input_feat4,Input_feat5,Input_feat6,Input_feat7,Input_feat8,Input_feat9,Input_feat10,Input_feat11,Input_feat12,Input_feat13,Input_feat14,Input_feat15,Input_feat16,Input_feat17,Input_feat18]).reshape(1,-1)
        to_predict=loadScaler.transform(to_predict)
        predict = loadModel.predict(to_predict)[0]
        proba = loadModel.predict_proba(to_predict)[0][predict]
        if predict == 0 :
            return html.Center(html.H1('The Employee is no Attrition with probability {}'.format(round(proba, 2))))
        else :
            return html.Center(html.H1('The Employee is Attrition with probability {}'.format(round(proba, 2))))


if __name__ == '__main__':
    app.run_server(debug=True)