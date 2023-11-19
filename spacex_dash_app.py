
# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                         options=[
                                         {'label': 'All Sites', 'value': 'ALL'},
                                         {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                         {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                         {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                         {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                                     ],
                                     value='ALL',
                                     placeholder="Select a Launch Site here",
                                     searchable=True
                                     ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                    min=0, max=10000, step=1000,
                                    marks={0: '0', 10000: '10000'},
                                    value=[min_payload, max_payload]
                                    ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def render_pie_chart(entered_site):
    if entered_site == 'ALL':
        # If 'ALL' sites are selected, calculate success counts for all sites
        all_sites_success_counts = spacex_df[spacex_df['class'] == 1]['Launch Site'].value_counts()
        all_sites_failed_counts = spacex_df[spacex_df['class'] == 0]['Launch Site'].value_counts()
        
        # Create a pie chart figure
        fig = px.pie(names=all_sites_success_counts.index, values=all_sites_success_counts,
                     title='Total Success Launches by Site (All Sites)')
        
        return fig
    else:
        # If a specific site is selected, filter the dataframe for that site
        site_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        
        # Calculate success and failure counts for the selected site
        site_success_counts = site_df[site_df['class'] == 1]['class'].count()
        site_failed_counts = site_df[site_df['class'] == 0]['class'].count()
        
        # Create a pie chart figure for the selected site
        fig = px.pie(names=['Success', 'Failure'], values=[site_success_counts, site_failed_counts],
                     title=f'Success vs. Failure for {entered_site}')
        
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id="payload-slider", component_property="value")])
def render_scatter_chart(selected_site, payload_range):
    if selected_site == 'ALL':
        # If 'ALL' sites are selected, filter the entire dataframe
        filtered_df = spacex_df
    else:
        # If a specific site is selected, filter the dataframe for that site
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
    
    # Filter the dataframe based on payload range
    filtered_df = filtered_df[(filtered_df['Payload Mass (kg)'] >= payload_range[0]) &
                              (filtered_df['Payload Mass (kg)'] <= payload_range[1])]
    
    # Create a scatter plot
    fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                     color='Booster Version Category',
                     title=f'Scatter Plot of Payload vs. Launch Outcome for {selected_site}')
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
