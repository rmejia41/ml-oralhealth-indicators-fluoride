# #Final app
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

# Set the theme to SOLAR
app_theme = dbc.themes.SANDSTONE #SOLAR PULSE SANDSTONE

# Load the dataset
df = pd.read_excel('https://github.com/rmejia41/open_datasets/raw/main/ML_state_oralhealthindicators.xlsx')

# Ensure state abbreviations are in uppercase to match Plotly's expectations
df['State'] = df['State'].str.upper()

# Initialize the Dash app with the selected theme
app = dash.Dash(__name__, external_stylesheets=[app_theme])
server = app.server

app.layout = html.Div([
    html.H1("Dashboard: Dental Health Outcomes, Fluoridation, and Unmet Dental Needs in the US",
            style={'textAlign': 'center', 'width': '70%', 'margin': '0 auto 20px', 'fontSize': '23px'}),
    html.Div([
        html.Div([
            html.Label('Select a Dental Outcome:', style={'display': 'block'}),
            dcc.Dropdown(
                id='dental-outcome-dropdown',
                options=[
                    {'label': 'Treated Untreated Decay', 'value': 'Treated Untreated Decay'},
                    {'label': 'Untreated Decay', 'value': 'Untreated Decay'},
                    {'label': 'Sealants', 'value': 'Sealants'}
                ],
                value='Sealants',
                style={'width': '70%'}
            )
        ], style={'width': '48%', 'display': 'inline-block', 'marginRight': '4%'}),  # Adjust marginRight to control spacing
        html.Div([
            html.Label('Select an Indicator:', style={'display': 'block'}),
            dcc.Dropdown(
                id='indicator-dropdown',
                options=[
                    {'label': 'Avg Fluoride Concentration 2020', 'value': 'Avg Fluoride Concentration 2020'},
                    {'label': 'Fluoridated Total 2020', 'value': 'Fluoridated Total 2020'},
                    {'label': 'Fluoridated Adjusted 2020', 'value': 'Fluoridated Adjusted 2020'},
                    {'label': 'Fluoridated Consecutive 2020', 'value': 'Fluoridated Consecutive 2020'},
                    {'label': 'Fluoridated Natural 2020', 'value': 'Fluoridated Natural 2020'},
                    {'label': 'Non Fluoridated 2020', 'value': 'Non Fluoridated 2020'},
                    {'label': 'Percent of Need Met', 'value': 'Percent of Need Met'},
                    {'label': 'Practitioners Needed to Remove HPSA Designation', 'value': 'Practitioners Needed to Remove HPSA Designation'}
                ],
                value='Avg Fluoride Concentration 2020',
                style={'width': '70%'}
            )
        ], style={'width': '48%', 'display': 'inline-block'})
    ], style={'display': 'flex', 'flexWrap': 'wrap'}),
    html.Div([
        dcc.Graph(id='choropleth-map'),
        dcc.Graph(id='correlation-plot')
    ], style={'display': 'flex'})
], style={'font-family': 'Arial, sans-serif'})

@app.callback(
    [Output('choropleth-map', 'figure'),
     Output('correlation-plot', 'figure')],
    [Input('dental-outcome-dropdown', 'value'),
     Input('indicator-dropdown', 'value')]
)
def update_graphs(selected_outcome, selected_indicator):
    # Filter out rows where the selected outcome or indicator is NaN
    filtered_df = df.dropna(subset=[selected_outcome, selected_indicator]).copy()

    # If the selected indicator is Avg Fluoride Concentration 2020, round it to 2 decimal places
    if selected_indicator == 'Avg Fluoride Concentration 2020':
        filtered_df[selected_indicator] = filtered_df[selected_indicator].round(2)

    # Generate the choropleth map
    map_figure = px.choropleth(
        filtered_df,
        locations='State',
        locationmode="USA-states",
        color=selected_outcome,
        hover_name='Location',  # Use full state names for hover
        hover_data={selected_indicator: True, 'Location': False},  # Include selected indicator in hover data, exclude Location since it's already used in hover_name
        scope="usa",
        title=f"{selected_outcome} by State"
    )

    # Generate the correlation plot
    plot_figure = px.scatter(
        filtered_df,
        x=selected_indicator,
        y=selected_outcome,
        trendline="ols",
        labels={
            selected_indicator: selected_indicator,
            selected_outcome: selected_outcome
        },
        title=f"Correlation between {selected_indicator} and {selected_outcome}"
    )

    return map_figure, plot_figure

# Run the app
if __name__ == '__main__':
    app.run_server(debug=False)
