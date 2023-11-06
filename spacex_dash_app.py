# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
launch_sites_list = list(spacex_df['Launch Site'].unique())
launch_sites_list.append('ALL')

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)

                                html.Div(dcc.Dropdown(
                                        id='select-launch-site',
                                        options=[{'label': i, 'value': i} for i in launch_sites_list],
                                        value='ALL'
                                    )),

                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)

                                dcc.RangeSlider(id='payload-slider', min=min_payload, max=max_payload,
                                step = 1000, value=[min_payload,max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
                Input(component_id='select-launch-site', component_property='value'))

def update_pie_chart(selected_launch_site):
    if selected_launch_site == 'ALL':
        pie_data = spacex_df[['Launch Site','class']].groupby('class').count().reset_index()
        pie_title = "Successful launches for all launch sites"
    else:
        pie_data = spacex_df.loc[spacex_df['Launch Site']==selected_launch_site,['Launch Site','class']].groupby('class').count().reset_index()
        pie_title = f"Successful launches for {selected_launch_site} launch site"
    fig=px.pie(pie_data,values='Launch Site',
                                names='class', color='class',
                                title=pie_title,color_discrete_map={'1':'lightcyan','0':'darkblue'})
    return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
            [Input(component_id='select-launch-site', component_property='value'), Input(component_id='payload-slider', component_property='value')])

def update_scatter_chart(selected_launch_site, selected_payload):
    payload_min, payload_max = selected_payload
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)']>=payload_min)&(spacex_df['Payload Mass (kg)']<=payload_max)]
    if selected_launch_site == 'ALL':
        scatter_data = filtered_df
        scatter_title = "Correlation between payload mass and success for all sites"
    else:
        scatter_data = filtered_df[filtered_df['Launch Site']==selected_launch_site]
        scatter_title = f"Correlation between payload mass and success for {selected_launch_site} launch site"
    fig=px.scatter(scatter_data,x='Payload Mass (kg)', y = 'class',
                                color = 'Booster Version',
                                title=scatter_title)
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
