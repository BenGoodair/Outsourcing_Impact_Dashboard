


from dash import Dash, State, html, dash_table, dcc, callback, Output, Input
import pandas as pd


import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

#import cdstoolbox as ct
#import chart_studio.plotly as py

import chart_studio.plotly as py
import dash_bootstrap_components as dbc




####Figure 2 - caro's mapppp#####

# Read the CSV file
final_daily2 = pd.read_csv('https://raw.githubusercontent.com/BenGoodair/Methane_Dashboard/main/combined_daily.csv')
simulated = pd.read_csv('https://raw.githubusercontent.com/BenGoodair/Methane_Dashboard/main/simulated_data.csv')
# Round 'lon_m' and 'lat_m' columns
final_daily2['lon_m'] = final_daily2['lon_m'].round()
final_daily2['lat_m'] = final_daily2['lat_m'].round()
# Convert 'time' column to datetime
final_daily2['date'] = pd.to_datetime(final_daily2['time']).dt.date
# Group by 'date', 'lon_m', and 'lat_m', and calculate the mean of 'ch4'
mean_ch4 = final_daily2.groupby(['date','lon_m', 'lat_m'])['ch4'].mean().reset_index()
# Remove rows with missing values
mean_ch4 = mean_ch4.dropna()

#convert date to date column
mean_ch4['date'] = pd.to_datetime(mean_ch4['date'])

#order data by date
mean_ch4.sort_values(by='date', ascending=False, inplace=True)
#keep only most recent data for each lon and lat
mean_ch4.drop_duplicates(subset=['lon_m', 'lat_m'], keep='first', inplace=True)
#reset
mean_ch4.reset_index(drop=True, inplace=True)

import plotly.graph_objects as go
from scipy.spatial import cKDTree

import plotly.express as px
import plotly.graph_objects as go

# Create a Plotly choropleth map


import plotly.graph_objects as go
import plotly.express as px
from scipy.spatial.distance import cdist
import numpy as np

hospitals = simulated[simulated['plant_or_hospital'] == "Hospital"]
hospitals = hospitals.rename(columns={'latitude': 'lat'})
hospitals = hospitals.rename(columns={'longitude': 'lon'})

energy_plants = simulated[simulated['plant_or_hospital'] == "Energy plant"]
energy_plants = energy_plants.rename(columns={'latitude': 'lat'})
energy_plants = energy_plants.rename(columns={'longitude': 'lon'})

import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from scipy.spatial import cKDTree


df_sorted = mean_ch4.sort_values('ch4', ascending=False)

# Calculate the number of rows representing the top 10%
top_10_percent = int(len(df_sorted) * 0.1)

# Slice the DataFrame to keep only the top rows
top_10_df = df_sorted.head(top_10_percent)

n = len(top_10_df)

# Create a new column 'Ascending' with values from 1 to n
top_10_df['USA_Methane_Ranking'] = range(1, n+1)

top_10_df = top_10_df.rename(columns={'lat_m': 'lat'})
top_10_df = top_10_df.rename(columns={'lon_m': 'lon'})


from scipy.spatial.distance import cdist

# Assuming 'hospitals' and 'top_10_df' are your DataFrames
# Assuming 'hospitals' has columns 'Hospital Name', 'Latitude', and 'Longitude'
# Assuming 'top_10_df' has columns 'Row ID', 'Latitude', and 'Longitude'

# Create a helper function to find the nearest hospital for a given location
def find_nearest_hospital(row, hospitals):
    # Create a DataFrame with coordinates of the current row
    coords = pd.DataFrame({'lat': [row['lat']], 'lon': [row['lon']]})

    # Calculate the distances between the coordinates of the current row and all hospitals
    distances = cdist(coords.values, hospitals[['lat', 'lon']].values, metric='euclidean')

    # Find the index of the nearest hospital
    nearest_index = distances.argmin()

    # Return the name of the nearest hospital
    return hospitals.iloc[nearest_index]['company_name']

# Apply the helper function to each row in 'top_10_df'
top_10_df['Nearest_Hospital'] = top_10_df.apply(lambda row: find_nearest_hospital(row, hospitals), axis=1)



# Create a helper function to find the nearest hospital for a given location
def find_nearest_plant(row, energy_plants):
    # Create a DataFrame with coordinates of the current row
    coords = pd.DataFrame({'lat': [row['lat']], 'lon': [row['lon']]})

    # Calculate the distances between the coordinates of the current row and all hospitals
    distances = cdist(coords.values, energy_plants[['lat', 'lon']].values, metric='euclidean')


    # Find the index of the nearest hospital
    nearest_index = distances.argmin()

    # Return the name of the nearest hospital
    return energy_plants.iloc[nearest_index]['company_name']

# Apply the helper function to each row in 'top_10_df'
top_10_df['Nearest_Energy_plant'] = top_10_df.apply(lambda row: find_nearest_plant(row, energy_plants), axis=1)





min_value = top_10_df['ch4'].min()
max_value = top_10_df['ch4'].max()
scaled_values = ((top_10_df['ch4'] - min_value) / (max_value - min_value)) ** 1.2 * 15

customdata = top_10_df[['USA_Methane_Ranking', 'Nearest_Hospital', 'Nearest_Energy_plant', 'ch4']].values.tolist()
customdata = np.stack((top_10_df['USA_Methane_Ranking'], top_10_df['Nearest_Hospital'], top_10_df['Nearest_Energy_plant'], top_10_df['ch4']), axis=-1)


# Create the scatter plot with scaled point sizes
tab1_fig2 = px.scatter_mapbox(top_10_df, lat="lat", lon="lon", hover_name="ch4",
                         size=scaled_values,
                         color_continuous_scale='viridis',
                         mapbox_style="carto-positron",
                         zoom=2,
                         center={'lat': 39.8283, 'lon': -98.5795},
                         opacity=0.8, size_max=30,    
                         custom_data=['USA_Methane_Ranking', 'Nearest_Hospital', 'Nearest_Energy_plant', 'ch4'])


tab1_fig2.update_traces(hovertemplate='Methane ranking: %{customdata[0]}<br>Nearest Hospital: %{customdata[1]}<br>Nearest Energy Plant: %{customdata[2]}<br>Methane particles (Mole fraction): %{customdata[3]}')






###############################################################################
######### ALL OF CAROLIN's CREATE FIGURE STUFF ##############################################
###############################################################################


# Carolin create figure tab2: methane emissions over time with state drop down 

import pandas as pd
import plotly.express as px

# Read the CSV file into a DataFrame
tab2_df_county = pd.read_csv('https://raw.githubusercontent.com/BenGoodair/Methane_Dashboard/main/methane_monthly_county.csv')

#tab2_df_county['date'] = pd.to_datetime(tab2_df_county['date'])


# Convert 'date' column to datetime data type
tab2_df_county['date'] = pd.to_datetime(tab2_df_county['date'])

tab2_FipsDF = pd.read_csv('https://raw.githubusercontent.com/BenGoodair/Methane_Dashboard/main/fips2county.tsv', sep='\t', header='infer', dtype=str, encoding='latin-1')
tab2_StateAbbrDF = tab2_FipsDF[["StateAbbr", 'StateFIPS', "StateName"]].drop_duplicates()

tab2_df_county = pd.merge(tab2_df_county, tab2_StateAbbrDF.astype({'StateFIPS': 'int64'}), left_on='STATEFP', right_on='StateFIPS', how='left')
#tab2_df_county['StateName'] = tab2_df_county['StateName'].astype('object')
tab2_df_county = tab2_df_county.dropna(subset=['StateName'])

tab2_df_county.head()



# Carolin create figure tab3: US Map for leaks with a date slider 

import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime

tab3_df_daily = pd.read_csv('https://raw.githubusercontent.com/BenGoodair/Methane_Dashboard/main/methane_final_lonlat.csv')
tab3_states = gpd.read_file('https://raw.githubusercontent.com/BenGoodair/Methane_Dashboard/main/gadm36_USA_1.shp')

tab_3_FipsDF = pd.read_csv('https://raw.githubusercontent.com/BenGoodair/Methane_Dashboard/main/fips2county.tsv', sep='\t', header='infer', dtype=str, encoding='latin-1')
tab3_StateAbbrDF = tab_3_FipsDF[["StateAbbr", 'StateFIPS', "StateName"]].drop_duplicates()

tab3_df_daily = pd.merge(tab3_df_daily, tab3_StateAbbrDF.astype({'StateFIPS': 'int64'}), left_on='STATEFP', right_on='StateFIPS', how='left')
tab3_df_daily['StateName'] = tab3_df_daily['StateName'].astype('object')
tab3_df_daily = tab3_df_daily.dropna(subset=['StateName'])

# Filter and sample the data
tab3_df_daily['date'] = pd.to_datetime(tab3_df_daily['date'])
tab3_df_daily['day_of_year'] = tab3_df_daily['date'].dt.dayofyear
tab3_df_daily['week_of_year'] = tab3_df_daily['date'].dt.isocalendar().week

tab3_df_filtered = tab3_df_daily[tab3_df_daily['date'].dt.year == 2019]













#ugggggh

df_county = pd.read_csv('https://raw.githubusercontent.com/BenGoodair/Methane_Dashboard/main/methane_monthly_county.csv')

df_county['date'] = pd.to_datetime(df_county['date'])


tab2_FipsDF = pd.read_csv('https://raw.githubusercontent.com/BenGoodair/Methane_Dashboard/main/fips2county.tsv', sep='\t', header='infer', dtype=str, encoding='latin-1')
tab2_StateAbbrDF = tab2_FipsDF[["StateAbbr", 'StateFIPS', "StateName"]].drop_duplicates()

df_county = pd.merge(df_county, tab2_StateAbbrDF.astype({'StateFIPS': 'int64'}), left_on='STATEFP', right_on='StateFIPS', how='left')
#tab2_df_county['StateName'] = tab2_df_county['StateName'].astype('object')
df_county = df_county.dropna(subset=['StateName'])

df_county.head()





####HEALTHY CAKES####


tab4_df = pd.read_csv("https://raw.githubusercontent.com/BenGoodair/Methane_Dashboard/main/month_health_df.csv")
# alter the mh ID to be "mental health"
tab4_df['ID'] = tab4_df['ID'].replace('mh', 'mental health')
import pandas as pd
import plotly.graph_objects as go
import plotly.colors as colors

tab4_df.sort_values(by='ID', ascending=False, inplace=True)




##fig 9 - county emissions and health##
import pandas as pd
import plotly.express as px
import geopandas as gpd

### Prepare each of the data frames and merge them ###
# Read CSV files
tab5_df_county = pd.read_csv('https://raw.githubusercontent.com/BenGoodair/Methane_Dashboard/main/methane_final_county.csv')
tab5_df_health = pd.read_csv('https://raw.githubusercontent.com/BenGoodair/Methane_Dashboard/main/month_health_df.csv')

tab5_df_county['month'] = pd.to_datetime(tab5_df_county['date']).dt.strftime('%m')
tab5_df_county['year'] = pd.to_datetime(tab5_df_county['date']).dt.strftime('%Y')

# STATE conversion 
state_abbr_dict = {
    '01': 'AL', '02': 'AK', '04': 'AZ', '05': 'AR', '06': 'CA', '08': 'CO', '09': 'CT', '10': 'DE',
    '11': 'DC', '12': 'FL', '13': 'GA', '15': 'HI', '16': 'ID', '17': 'IL', '18': 'IN', '19': 'IA',
    '20': 'KS', '21': 'KY', '22': 'LA', '23': 'ME', '24': 'MD', '25': 'MA', '26': 'MI', '27': 'MN',
    '28': 'MS', '29': 'MO', '30': 'MT', '31': 'NE', '32': 'NV', '33': 'NH', '34': 'NJ', '35': 'NM',
    '36': 'NY', '37': 'NC', '38': 'ND', '39': 'OH', '40': 'OK', '41': 'OR', '42': 'PA', '44': 'RI',
    '45': 'SC', '46': 'SD', '47': 'TN', '48': 'TX', '49': 'UT', '50': 'VT', '51': 'VA', '53': 'WA',
    '54': 'WV', '55': 'WI', '56': 'WY'
}

tab5_df_county['STATE'] = tab5_df_county['STATEFP'].map(state_abbr_dict)

tab5_map_data = gpd.read_file('https://raw.githubusercontent.com/BenGoodair/Methane_Dashboard/main/cb_2018_us_county_500k.shp')

# Select desired columns
tab5_map_data = tab5_map_data.drop(columns='geometry')[['COUNTYNS', 'GEOID', 'NAME']]

# Housekeeping conversions for data type compatibility
# Convert COUNTYNS column to int64
tab5_map_data['COUNTYNS'] = tab5_map_data['COUNTYNS'].astype(int)

# Convert COUNTYNS column in df_county to int64 if needed
tab5_df_county['COUNTYNS'] = tab5_df_county['COUNTYNS'].astype(int)

# Merge mapdata with with df_county
tab5_df_county = pd.merge(tab5_map_data, tab5_df_county, on='COUNTYNS')


# Define a lookup table for month abbreviations and corresponding numerical values
month_lookup = {
    "Jan.": "01", "Feb.": "02", "Mar.": "03", "Apr.": "04",
    "May": "05", "Jun.": "06", "Jul.": "07", "Aug.": "08",
    "Sep.": "09", "Oct.": "10", "Nov.": "11", "Dec.": "12"
}

# Convert the month column to numerical values
tab5_df_health['month'] = tab5_df_health['Month'].map(month_lookup)

tab5_df_health['County Code'] = tab5_df_health['County Code'].astype(int)
tab5_df_health['County Code'] = tab5_df_health['County Code'].astype(str).str.zfill(5)
tab5_df_health.rename(columns={'County Code': 'GEOID', 'Year Code': 'year'}, inplace = True)

# Convert 'GEOID' column in df_county to string
tab5_df_county['GEOID'] = tab5_df_county['GEOID'].astype(str)

# Check for non-numeric values in 'GEOID' column
non_numeric_values = tab5_df_county[~tab5_df_county['GEOID'].str.isdigit()]['GEOID'].unique()
print(f"Non-numeric values in 'GEOID' column: {non_numeric_values}")

# Remove non-numeric values from df_county
tab5_df_county = tab5_df_county[tab5_df_county['GEOID'].str.isdigit()]

# Convert 'GEOID' column to integer
tab5_df_county['GEOID'] = tab5_df_county['GEOID'].astype(int)
tab5_df_health['GEOID'] = tab5_df_health['GEOID'].astype(int)

# Group by 'GEOID', 'month', and 'year' and calculate mean of 'mean_ch4'
tab5_df_county_grouped = tab5_df_county.groupby(['GEOID', 'month', 'year'])['mean_ch4'].mean().reset_index()

# Drop invalid observations containing non-finite values
tab5_df_health['year'] = tab5_df_health['year'].dropna().astype(float)

# Fill remaining NaN values with a default value (e.g., 0)
tab5_df_health['year'].fillna(0, inplace=True)

# Convert the column to integer
tab5_df_health['year'] = tab5_df_health['year'].astype(int)

# Convert the column to object (string)
tab5_df_health['year'] = tab5_df_health['year'].astype(str)

### Create final data frame ###
# Merge DataFrames based on 'GEOID', 'month', and 'year'
tab5_combined = pd.merge(
    tab5_df_health,
    tab5_df_county_grouped,
    on=['GEOID', 'month', 'year']
)


### Create the figure ###

tab5_fig = px.scatter(tab5_combined[tab5_combined['ID'] == 'methane'], x='mean_ch4', y='Deaths',
                 title='Methane-related deaths in the US',
                 labels={'mean_ch4': 'Average county-level methane emissions', 'Deaths': 'Deaths per month'})

tab5_fig.update_layout(
    xaxis_title='Average county-level methane emissions',
    yaxis_title='Deaths per month',
    title='Methane-related deaths in the US'
)

# Define coordinates for the rectangular shape
x0, x1 = 1900, tab5_fig['data'][0]['x'].max()  # x-axis range
y0, y1 = 50, tab5_fig['data'][0]['y'].max()  # y-axis range

# Add a red rectangular shape
tab5_fig.add_shape(type='rect',
              xref='x', yref='y',
              x0=x0, y0=y0,
              x1=x1, y1=y1,
              line=dict(color='red', width=2),
              fillcolor='rgba(0,0,0,0)',  # Transparent fill
              opacity=1)

# Update hovertemplate to display county names
tab5_fig.update_traces(hovertemplate='Mean CH4: %{x}<br>'
                                'Deaths: %{y}<br>'
                                'County: %{customdata}<extra></extra>',
                  customdata=tab5_combined[tab5_combined['ID'] == 'methane']['County'],
                  hoverlabel=dict(namelength=0))

##fig 8 - methane-related deaths stratified by race##
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

tab6_df = pd.read_csv('https://raw.githubusercontent.com/BenGoodair/Methane_Dashboard/main/Race_Methane.txt', delimiter='\t')

tab6_df = tab6_df.groupby(['County', 'Single Race 6'])['Deaths'].sum().reset_index()

tab6_df['total_deaths'] = tab6_df.groupby('County')['Deaths'].transform('sum')

tab6_df['Proportion'] = tab6_df['Deaths'] / tab6_df['total_deaths']

tab6_df.sort_values(by='Single Race 6', ascending=True, inplace=True)

##### search function#####

#import cdsapi

# c = cdsapi.Client(url = "...", key = "...")

# c.retrieve(
#     'satellite-methane',
#     {
#         'processing_level': 'level_2',
#         'variable': 'ch4',
#         'sensor_and_algorithm': 'iasi_metop_b_nlis',
#         'year': '2019',
#         'month': '07',
#         'day': '11',
#         'version': '9.1',
#         'format': 'zip',
#     },
#     '/Users/carolinkroeger/Library/CloudStorage/OneDrive-Nexus365/GitHub/Climate_Coders/data/download.zip')


## Get location 

from geopy.geocoders import Nominatim

# calling the Nominatim tool
loc = Nominatim(user_agent="GetLoc")

# entering the location name
getLoc = loc.geocode("my_location")

target_address = getLoc.address
target_lon = getLoc.longitude
#target_lon = round(target_lon, 2)
target_lat = getLoc.latitude
#target_lat = round(target_lat, 2)

# Find closest methane observation 

import netCDF4 as nc
import pandas as pd
from geopy.distance import geodesic

# Open the netCDF file
df_search = pd.read_csv('https://raw.githubusercontent.com/BenGoodair/Methane_Dashboard/main/df_find_location.csv')



# Function to calculate distance between two points
def calculate_distance(lon1, lat1, lon2, lat2):
    point1 = (lat1, lon1)
    point2 = (lat2, lon2)
    distance = geodesic(point1, point2).miles
    return distance

# Calculate distances between target point and all points in the data frame
distances = df_search.apply(lambda row: calculate_distance(target_lon, target_lat, row['longitude'], row['latitude']), axis=1)

# Find the index of the closest point
closest_index = distances.idxmin()

# Retrieve the closest matching point
closest_point = df_search.loc[closest_index]

# Print the result
print(closest_point) # target_address, 
















































####Dashboard####
#app = Dash(__name__)
import dash 
from dash import dash_table
from dash import State
import reverse_geocoder as rg
from dash.dependencies import Input, Output, State, MATCH



app = dash.Dash(external_stylesheets=[dbc.themes.LUX])

#server = app.server

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Methane Impacts Tracker", className="display-7"),
        html.Hr(),
        html.P(
            "Welcome to a dashboard detailing the health impacts of methane exposure in the USA.", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Methane Emissions", href="/page-1", active="exact"),
                dbc.NavLink("Health Impacts", href="/page-2", active="exact"),
                dbc.NavLink("Links To Resources", href="/page-3", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)


def generate_top_locations_table():
    # Sort the dataframe by 'ch4' column in descending order and select the top 10 rows
    top_locations = top_10_df.sort_values('ch4', ascending=False).head(10)
    
    # Use reverse geocoding to obtain the US state based on latitude and longitude
    coordinates = list(zip(top_locations['lat'], top_locations['lon']))
    state_info = rg.search(coordinates)
    us_states = [info['admin1'] for info in state_info]
    
    # Add the 'US State' column to the dataframe
    top_locations['US State'] = us_states

    top_locations = top_locations[['USA_Methane_Ranking', 'US State', 'ch4', 'Nearest_Energy_plant', 'Nearest_Hospital', 'lon', 'lat', 'date']]

    top_locations['ch4'] = top_locations['ch4'].round(2)

    top_locations.columns = [col.replace('_', ' ') for col in top_locations.columns]
    
    # Rename 'ch4' column to 'Methane particles (Mole fraction)'
    top_locations.rename(columns={'ch4': 'Methane particles (Mole fraction)'}, inplace=True)
    
    # Create a Dash DataTable component
    table = dash_table.DataTable(
        id='top-locations-table',
        columns=[{'name': col, 'id': col} for col in top_locations.columns],
        data=top_locations.to_dict('records'),
        style_data={'whiteSpace': 'normal', 'height': 'auto'},
        style_table={'overflowX': 'auto'},
    )
    
    return table

def generate_action_plan_textbox(tab):
    if tab == 'tab-1':
        content = html.Div([
            html.P("Action plan for policymakers in relation to methane leaks:",
                style={"font-size": "28px", "padding-left": "28px"}),
            html.Ul([
                html.Li("Locate leaks based on highest dectated methane levels"),
                html.Li("Phone nearest energy company to ask them to check piping"),
                html.Li("Warn hospital and employers of potential health risks for staff"),
                ],
                style={"font-size": "28px", "padding-left": "28px"}
            )
        ])
    elif tab == 'tab-2':
        content = html.Div([
            html.P("Action plan for policymakers in relation to environmental methane increases:",
                style={"font-size": "28px", "padding-left": "28px"}),
            html.Ul([
                html.Li("Lobby to prevent increases in methane levels in your state."),
                html.Li("Think about the future trajectory if nothing is done to mitigate methane levels."),
                html.Li("Read up on why methane is concerning for health and wellbeing of populations (see our resource list)"),
                ],
                style={"font-size": "28px", "padding-left": "28px"}
            )
        ])
    elif tab == 'tab-3':
        content = html.Div([
            html.P("Action plan for policymakers in relation to methane geographies:",
                style={"font-size": "28px", "padding-left": "28px"}),
            html.Ul([
                html.Li("See the methane levels in your local area and how that is changing."),
                html.Li("Mobilise resources to those areas to help mitigate impacts of methane."),
                html.Li("Think about whether there are natural or unnatural reasons for those methane levels and what can be done to lower them."),
                ],
                style={"font-size": "28px", "padding-left": "28px"}
            )
        ])
    elif tab == 'tab-4':
        content = html.Div([
            html.P("Action plan for policymakers in relation to methane geographies:",
                style={"font-size": "28px", "padding-left": "28px"}),
            html.Ul([
                html.Li("See the methane levels in your local area and how that is changing."),
                html.Li("Mobilise resources to those areas to help mitigate impacts of methane."),
                html.Li("Think about whether there are natural or unnatural reasons for those methane levels and what can be done to lower them."),
                ],
                style={"font-size": "28px", "padding-left": "28px"}
            )
        ])
    elif tab == 'tab-5':
        content = html.Div([
            html.P("Action plan for policymakers in relation to increasing risk of methane mortality.",
                style={"font-size": "28px", "padding-left": "28px"}),
            html.Ul([
                html.Li("See the rising human cost of methane."),
                html.Li("Work to reduce the short-term risks of methane exposure"),
                html.Li("Inform people about their own risk, according to their exposure levels (using geographic data in this dashboard)"),
                ],
                style={"font-size": "28px", "padding-left": "28px"}
            )
        ])
    elif tab == 'tab-6':
        content = html.Div([
            html.P("Action plan for policymakers in relation to at-risk counties.",
                style={"font-size": "28px", "padding-left": "28px"}),
            html.Ul([
                html.Li("Find the counties with highest methane exposures and worst health risks."),
                html.Li("Consider why those areas are worst impacted."),
                html.Li("Plan to reduce the impact in those counties."),
                ],
                style={"font-size": "28px", "padding-left": "28px"}
            )
        ])
    elif tab == 'tab-7':
        content = html.Div([
            html.P("Action plan for policymakers in relation to racial risk of methane mortality.",
                style={"font-size": "28px", "padding-left": "28px"}),
            html.Ul([
                html.Li("See who is being impacted most by methane exposure in your area."),
                html.Li("Consider why certain populations are being impacted more than others."),
                html.Li("Work to reduce inequalities and support communities most affected."),
                ],
                style={"font-size": "28px", "padding-left": "28px"}
            )
        ])

    return html.Div([
        html.Button(
            "Action Plan",
            id={'type': 'action-plan-btn', 'tab': tab},
            className="btn btn-primary",
            style={"margin-bottom": "1rem"},
        ),
        dbc.Collapse(
            content,
            id={'type': 'action-plan-collapse', 'tab': tab},
            is_open=False,
        )
    ])


@app.callback(Output({'type': 'action-plan-collapse', 'tab': MATCH}, 'is_open'),[Input({'type': 'action-plan-btn', 'tab': MATCH}, 'n_clicks')], [State({'type': 'action-plan-collapse', 'tab': MATCH}, 'is_open')])
def toggle_action_plan_collapse(n_clicks, is_open):
    if n_clicks is not None:
        return not is_open
    return is_open

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


# Define the callback function to update the plot for environmental justice based on dropdown selection
@app.callback(
    Output('tab6-plot', 'figure'),
    [Input('race-dropdown', 'value')]
)
def update_tab6_plot(selected_race):
    if selected_race is None:
        tab6_filtered_df = tab6_df[tab6_df['Single Race 6']]
    else:
        tab6_filtered_df = tab6_df[tab6_df['Single Race 6'] == selected_race]

    tab6_sorted_df = tab6_filtered_df.sort_values(by='Proportion', ascending=False)
    
    # Get the viridis color scale
    viridis_colors = colors.sequential.Viridis

    tab6_fig = px.scatter(tab6_sorted_df, x='County', y='Proportion', 
                     color='Single Race 6', color_discrete_sequence=viridis_colors, 
                     hover_data={'Single Race 6': False, 'Deaths': True},
                     labels={'Single Race 6': 'Race', 'Deaths': 'Number of Deaths'})

    tab6_fig.update_layout(
        title='Proportion of Deaths by County',
        xaxis_title='County',
        yaxis_title='Proportion of Deaths'
    )

    return tab6_fig


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.Div([
            html.H2("Welcome to the Methane Impacts Tracker Dashboard", className="display-7"),
            html.Hr(),
            html.H4("Purpose of the Dashboard"),
            html.P("The Climate Coders Methane Dashboard aims to provide policymakers with valuable insights into methane levels and their impact on population health in the USA. By visualizing methane emissions, health data, and related information, this dashboard assists policymakers in making informed decisions to address the challenges posed by methane exposure."),
            html.H4("Key Features"),
            html.Ul([
                html.Li("Methane Leaks: Interactive map showcasing highest methane emissions and nearby energy sites."),
                html.Li("Rising Methane Emmissions: Graphical representations and visualizations of localised methane data trends."),
                html.Li("Methane Map: See where and when methane emmissions are highest."),
                html.Li("Increasing risks of methane-related health: Graphical visualisation in trends of respiratory, mental health and methane mortalities."),
                html.Li("Counties at health-risk: Identify which counties have highest methane and worst health outcomes."),
                html.Li("Racial impacts of methane emmissions: Graphs presenting methane-related mortalities and racial inequalities."),
                html.Li("Links to Resources: Comprehensive list of resources, papers, and articles related to methane emissions and impacts on health."),
            ]),
            html.H4("How to Use"),
            html.P("Navigate through the tabs at the sidebar to access different sections of the dashboard. Each section provides specific information and visualizations related to methane levels and health impacts. Use the interactive components to explore the data and gain insights."),
            html.P("We encourage policymakers to utilize this dashboard as a resource for evidence-based decision-making. By considering the data, visualizations, and resources provided here, policymakers can better understand the magnitude of methane emissions and the potential health risks associated with it. Additionally, we recommend referring to the 'Links to Resources' section for further in-depth research and reports."),
            html.Hr(),
            html.H4("Important Note"),
            html.P("This dashboard is for informational purposes only and should not be used as the sole basis for policymaking. It is crucial to consult domain experts, conduct further analysis, and consider additional factors when making policy decisions."),
            html.Hr(),
            html.H5("For more information, please visit the following pages:"),
            dbc.Nav(
                [
                    dbc.NavLink("Methane Emissions", href="/page-1", active="exact"),
                    dbc.NavLink("Health Impacts", href="/page-2", active="exact"),
                    dbc.NavLink("Links to Resources", href="/page-3", active="exact"),
                ],
                vertical=True,
                pills=True,
            ),
            html.Hr(),
            html.P("Acknowledgements: we are grateful to the support from Wellcome Trust who motivated this dashboard."),
        ], style={"padding": "2rem"})
    elif pathname == "/page-1":
        return html.Div([
            dcc.Tabs(id="page-1-tabs", value='tab-1', children=[
                dcc.Tab(label='Methane leaks', value='tab-1', style=tab_style, selected_style=tab_selected_style),
                dcc.Tab(label='Methane trends', value='tab-2', style=tab_style, selected_style=tab_selected_style),
                dcc.Tab(label='Methane geographies', value='tab-3', style=tab_style, selected_style=tab_selected_style),
            ], style=tabs_styles),
            html.Div(id='page-1-tabs-content')
        ])
    elif pathname == "/page-2":
        return html.Div([
            dcc.Tabs(id="page-2-tabs", value='tab-4', children=[
                dcc.Tab(label='Methane-related deaths', value='tab-4', style=tab_style, selected_style=tab_selected_style),
                dcc.Tab(label='At-risk counties', value='tab-5', style=tab_style, selected_style=tab_selected_style),
                dcc.Tab(label='Racial inequalities', value='tab-6', style=tab_style, selected_style=tab_selected_style),
            ], style=tabs_styles),
            html.Div(id='page-2-tabs-content')
        ])
    elif pathname == "/page-3":
        return html.Div([
            dcc.Tabs(id="page-3-tabs", value='tab-7', children=[
                dcc.Tab(label='Data download', value='tab-7', style=tab_style, selected_style=tab_selected_style),
                dcc.Tab(label='Data upload', value='tab-8', style=tab_style, selected_style=tab_selected_style),
                dcc.Tab(label='Educational resources', value='tab-9', style=tab_style, selected_style=tab_selected_style),
                dcc.Tab(label='Contact and feedback', value='tab-10', style=tab_style, selected_style=tab_selected_style),
            ], style=tabs_styles),
            html.Div(id='page-3-tabs-content')
        ])
   # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognized..."),
        ],
        className="p-3 bg-light rounded-3",
    )


@app.callback(Output('page-1-tabs-content', 'children'), [Input('page-1-tabs', 'value')])
def render_page_1_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H3('Find polluting plants and nearby hospitlas:'),
            dcc.Graph(id='map', style={'height': '800px'}),
            html.H4('Top Locations by Methane Levels'),
            generate_top_locations_table(),
            generate_action_plan_textbox('tab-1')
         ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3('See rising methane in your state:'),
            dcc.Dropdown(
                id='county-dropdown',
                options=[{'label': StateName, 'value': StateName} for StateName in df_county['StateName'].unique()],
                value=None,
                placeholder='Select a state',
                style={'width': '200px', 'margin-bottom': '20px'}
            ),
            dcc.Graph(
                id='scatter-plot'
            ),
            generate_action_plan_textbox('tab-2')
        ])
    elif tab == 'tab-3':
        return html.Div([
            html.H3('Find out where and when methane rises:'),
            dcc.Dropdown(
                id='state-dropdown',
                options=sorted([{'label': StateName, 'value': StateName} for StateName in tab3_df_filtered['StateName'].unique()], key=lambda x: x['label']),
                value=tab3_df_filtered['StateName'].unique()[0]
            ),
            dcc.Graph(id='map-graph', style={'height': '600px'}),
            html.H3('Select week of the year:'),
            dcc.Slider(
                id='date-slider',
                min=tab3_df_filtered['week_of_year'].min(),
                max=tab3_df_filtered['week_of_year'].max(),
                value=tab3_df_filtered['week_of_year'].min(),
                marks={str(week_of_year): str(week_of_year) for week_of_year in tab3_df_filtered['week_of_year'].unique()},
                step=None
            ),
            generate_action_plan_textbox('tab-3')
        ])


@app.callback(Output('page-2-tabs-content', 'children'), [Input('page-2-tabs', 'value')])
def render_page_2_content(tab):
    if tab == 'tab-4':
        return  html.Div([
            html.H3('See the increasing risk of death from methane exposure and related causes:'),
            dcc.Dropdown(
                id='death-type-dropdown',
                options=[{'label': death, 'value': death} for death in tab4_df['ID'].unique()],
                value=None,
                placeholder='Select a cause of death'
            ),
            dcc.Graph(id='tab4-plot'),
            generate_action_plan_textbox('tab-4')

        ])
    elif tab == 'tab-5':
        return html.Div([
            html.H3('Find out which counties have high emissions and mortalities:'),
            dcc.Graph(id='Health visualisation', figure=tab5_fig),
            generate_action_plan_textbox('tab-5')


        ])
    elif tab == 'tab-6':
        return  html.Div([
            html.H3('Find out which counties have high emissions and mortalities:'),
            dcc.Dropdown(
                id='race-dropdown',
                options=[{'label': race, 'value': race} for race in tab6_df['Single Race 6'].unique()],
                value=None,
                placeholder='Select a race'
            ),
            dcc.Graph(id='tab6-plot'),
            generate_action_plan_textbox('tab-6')
            
        ])




@app.callback(Output('page-3-tabs-content', 'children'), [Input('page-3-tabs', 'value')])
def render_page_3_content(tab):
    if tab == 'tab-7':
        return  html.Div([
            html.H3('Data Downloads:'),
            html.P('You can access to three different files: Data at the lat/llon scale, county scale or state scale:'),
            html.Ul([
                html.Li(html.A("Download Methane Data with latitude and longitude", href="https://raw.githubusercontent.com/BenGoodair/Methane_Dashboard/main/methane_final_lonlat.csv")),
                html.Li(html.A("Download Health Data for US Counties", href="https://raw.githubusercontent.com/BenGoodair/Methane_Dashboard/main/methane_final_county.csv")),
                html.Li(html.A("Download Health Data for US States", href="https://raw.githubusercontent.com/BenGoodair/Methane_Dashboard/main/methane_final_county.csv"))]),            
            html.H3('Data notes and licensing'),
            html.H6('Data sources used in this dashboard'),
            html.Ul([
                html.Li(html.A("The Copernicus Climate Data Store provides satellite-collected methane data ", href="https://cds.climate.copernicus.eu/cdsapp#!/dataset/satellite-methane?tab=overview")),
                html.Li(html.A("Health data comes from the Centre for Disease control and Prevention (CDC Wonder)", href="https://wonder.cdc.gov/ucd-icd10-expanded.html")),
                html.Li(html.A("Data on energy plants and hospitals is simulated and available here", href="https://raw.githubusercontent.com/BenGoodair/Methane_Dashboard/main/simulated_data.csv"))]),            
            html.H6('Potential Biases in data'),
            html.P('Please consider the following when interpretting our dashboard:'),
            html.Ul([
                html.Li("Health data and reporting follows on from histories of colonial measurement of health - as such we should be critical of racialised categories and minoritising or othering data."),
                html.Li("Data reflects global power hierachies and as such high-income countries are frequenlty over-represented.")]),
            html.H6('Data licenses for use and reuse'),
            html.P('Terms of use for the methane data are that:'),
            html.Ul([
                html.Li("We agree ... to inform us prior to any publication where the data products are planned to be used."),
                html.Li("We agree ... to offer us co-authorship for any planned peer-reviewed publication based on our data products.")]),
            html.P("Terms of use for the health data are that:"),
            html.Ul([
                html.Li("These data are provided for the purpose of statistical reporting and analysis only. The CDC/ATSDR Policy on Releasing and Sharing Data prohibits linking these data with other data sets or information for the purpose of identifying an individual."),
                html.Li("The Public Health Service Act (42 U.S.C. 242m(d)) provides that the data collected by the National Center for Health Statistics (NCHS) may be used only for the purpose for which they were obtained; any effort to determine the identity of any reported cases, or to use the information for any purpose other than for statistical reporting and analysis, is against the law.")])

        ])
    elif tab == 'tab-8':
        return  html.Div([
            html.H3('Methane data search:'),
            html.H6('Search for closest methane area anywhere in the world!'),
            html.Label('Enter a location:'),
            dcc.Input(id='location-input', type='text', placeholder='Enter a location'),
            html.Hr(),
            html.H6('Search results: (this feature will take around 15 seconds)'),
            html.Div(id='result-output'),
            html.Hr(),
            html.H3('Data upload:'),
            html.P('Soon you can upload your own data to merge it with methane and health data in this dashboard:'),
            html.Ul([
                html.Li("Data will use google API to search you data with the column labelled geography"),
                html.Li("Our code will then merge this with the closest methane and health data"),
                html.Li("Data will be returned in the format of your own choosing and will not be stored on our site."),            
                html.Li("This feature is in progress will eventually be deployed to this page.")])            
           ])
    elif tab == 'tab-9':
        return html.Div([
            html.H3("Links to Resources"),

            html.H6("Information on Methane and Research on its Rising Levels"),
            html.P("Learn about studies showing the rising methane levels over time and their impact on the environment:"),
            html.Ul([
                html.Li(html.A("What is methane and why does it matter?", href="https://www.epa.gov/gmi/importance-methane")),
                html.Li(html.A("Research on the dangerously fast growing methane levels", href="https://www.nature.com/articles/d41586-022-00312-2"))
            ]),

            html.H6("Impact of Methane on Human Health"),
            html.P("Discover the effects of methane on human health and related research findings:"),
            html.Ul([
                html.Li(html.A("Summary of the impacts of methane on human health", href="https://globalcleanair.org/methane-and-health/")),
                html.Li(html.A("Review on the impacts of methane on climate, health, and ecosystems", href="https://www-sciencedirect-com.ezproxy-prd.bodleian.ox.ac.uk/science/article/pii/S1462901122001204")),
                html.Li(html.A("Visual summary of the harmful impacts of methane", href="https://www.ccacoalition.org/es/slcps/methane"))
            ]),

            html.H6("Litigation of Gas Leaks in the USA"),
            html.P("Explore legal cases and actions related to gas leaks in the United States:"),
            html.Ul([
                html.Li(html.A("Report on climate litigation following a major gas leak", href="https://www.reuters.com/business/energy/socalgas-settles-2015-gas-leak-litigation-take-11-bln-charge-2021-09-27/"))
            ])
        ])
    elif tab == 'tab-10':
        return html.Div([
            html.H3("Meet the team:"),
            html.Ul([
                html.Li([
                    html.Img(src="https://github.com/BenGoodair/Methane_Dashboard/blob/main/carolin.jpg?raw=true", style={"width": "100px", "height": "100px"}),
                    html.Div([
                        html.H4("Carolin"),
                        html.P("Carolin is a social scientist working on identifying the short-term impacts of heat on the health of populations around the world."),
                        html.P("Carolin has led our team, setting out values of fun, cooperation, and kindness from the very start. We love her for this!")
                    ], style={"display": "inline-block", "vertical-align": "top"})
                ]),
                html.Li([
                    html.Img(src="https://github.com/BenGoodair/Methane_Dashboard/blob/main/dunja.jpg?raw=true", style={"width": "100px", "height": "100px"}),
                    html.Div([
                        html.H4("Dunja"),
                        html.P("Dunja is an engineer by training and has expertise in digital health."),
                        html.P("Dunja conducted a lot of this work from a sunbed in Greece, we think the sun matches her personality and shines through her work.")
                    ], style={"display": "inline-block", "vertical-align": "top"})
                ]),
                html.Li([
                    html.Img(src="https://github.com/BenGoodair/Methane_Dashboard/blob/main/ben.jpg?raw=true", style={"width": "100px", "height": "100px"}),
                    html.Div([
                        html.H4("Ben"),
                        html.P("Ben is a social researcher identifying the impacts of privatization on health and social care systems."),
                        html.P("Ben provided the baked goods for joint study sessions and is committed to doing so in the future.")
                    ], style={"display": "inline-block", "vertical-align": "top"})
                ])
            ]),
            html.H3("Partner with us:"),
            html.H6("Join our team to continue this work"),
            html.P("We are looking for partners with policy, industrial or lived experiences to join our happy community!"),
            html.Ul([
                html.Li('We will write a funding application to ensure labor compensated and valued.'),
                html.Li('We want new directions and ideas, bring your creativity!'),
                html.Li('We want to have fun and work in a respectful, supportive, and positive way.')
            ]),
            html.H3("Contact and feedback"),
            html.H6("Help us improve this dashboard for your needs!"),
            html.P("All our work is completely open access and reproducible, we'd love to work with you to apply this work to other data"),
            html.Ul([
                html.Li('Email us at: climate.codersemail.co.uk'),
                html.Li('Tweet us at: ClimateCoders'),
                html.Li('Find us at: ClimateCoders hub, United Kingdom')
            ])
        ])





def find_nearest_point(lat, lon, df):
    point = np.array([[lat, lon]])
    distances = cdist(point, df[['lat', 'lon']])
    nearest_index = np.argmin(distances)
    nearest_point = df.iloc[nearest_index]
    return nearest_point



# Define the callback function to update the scatter plot based on the dropdown selection
@app.callback(Output('map', 'figure'),[Input('map', 'clickData')])
def update_nearest_hospital(click_data):
    if click_data:
        point = click_data['points'][0]

        lat = point['lat']
        lon = point['lon']

        nearest_hospital = find_nearest_point(lat, lon, hospitals)
        nearest_energy_plant = find_nearest_point(lat, lon, energy_plants)

        # Create a new figure with the nearest hospital and energy plant annotations
        new_fig = go.Figure(tab1_fig2)

        new_fig.add_trace(
            go.Scattermapbox(
                lat=[lat, nearest_hospital['lat']],
                lon=[lon, nearest_hospital['lon']],
                mode='lines',
                line=dict(color='red', width=2),
                hoverinfo='none'
            )
        )
        new_fig.add_trace(
            go.Scattermapbox(
                lat=[lat, nearest_energy_plant['lat']],
                lon=[lon, nearest_energy_plant['lon']],
                mode='lines',
                line=dict(color='blue', width=2),
                hoverinfo='none'
            )
        )
        new_fig.add_trace(
            go.Scattermapbox(
                lat=[nearest_hospital['lat']],
                lon=[nearest_hospital['lon']],
                mode='markers',
                customdata=np.dstack((nearest_hospital["company_name"], nearest_hospital["phone_number"], nearest_hospital["number_of_employees"], nearest_hospital["previous_leaks_n"], nearest_hospital["fossil_fuel_type"], nearest_hospital["number_of_beds"])),
                marker=dict(size=10, color='red'),
                hovertemplate='Company Name: %{customdata[0][0]}<br>Company telephone: %{customdata[0][1]}<br>Number of Employees: %{customdata[0][2]}<br>Number of Previous Leaks: %{customdata[0][3]}<br>Fossil Fuel Type: %{customdata[0][4]}<br>Number of Hospital Beds: %{customdata[0][5]}'
            )
        )
        new_fig.add_trace(
            go.Scattermapbox(
                lat=[nearest_energy_plant['lat']],
                lon=[nearest_energy_plant['lon']],
                mode='markers',
                customdata=np.dstack((nearest_energy_plant["company_name"], nearest_energy_plant["phone_number"], nearest_energy_plant["number_of_employees"], nearest_energy_plant["previous_leaks_n"], nearest_energy_plant["fossil_fuel_type"], nearest_energy_plant["number_of_beds"])),
                marker=dict(size=10, color='blue'),
                hovertemplate='Company Name: %{customdata[0][0]}<br>Company telephone: %{customdata[0][1]}<br>Number of Employees: %{customdata[0][2]}<br>Number of Previous Leaks: %{customdata[0][3]}<br>Fossil Fuel Type: %{customdata[0][4]}<br>Number of Hospital Beds: %{customdata[0][5]}'
            )   
        )
       # Set the zoom and view location from the previous figure
        new_fig.update_layout(mapbox=dict(center=dict(lat=tab1_fig2['layout']['mapbox']['center']['lat'],
                                                      lon=tab1_fig2['layout']['mapbox']['center']['lon']),
                                               zoom=tab1_fig2['layout']['mapbox']['zoom']))

        return new_fig

    return tab1_fig2




@app.callback(Output('scatter-plot', 'figure'),[Input('county-dropdown', 'value')])
def update_scatter_plot(selected_county):
    if selected_county is None:
        filtered_df = df_county
    else:
        filtered_df = df_county[df_county['StateName'] == selected_county]

    fig = px.scatter(filtered_df, x='date', y='ch4', color='ch4', trendline='lowess')
    fig.update_traces(marker=dict(size=5))
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Methane ppm',
        title='Rising methane emissions in the United States (2003-2021)',
        coloraxis_colorbar=dict(title='Methane ppb')
    )
    
    return fig





# Carolin callback tab3 tab3_fig: map with emissions in 2019 and date slider and state drop down
@app.callback(dash.dependencies.Output('map-graph', 'figure'),[dash.dependencies.Input('date-slider', 'value'),dash.dependencies.Input('state-dropdown', 'value')])
def update_map(selected_date, selected_state):
    tab3_filtered_data = tab3_df_filtered[(tab3_df_filtered['week_of_year'] == selected_date) & (tab3_df_filtered['StateName'] == selected_state)]

    tab3_fig = px.scatter_mapbox(tab3_filtered_data, lat='latitude', lon='longitude',
                            hover_data=['ch4'], color='ch4', color_continuous_scale='Viridis',
                            range_color=[tab3_df_filtered['ch4'].min(), tab3_df_filtered['ch4'].max()],
                            size='ch4', size_max=10, zoom=3)

    tab3_fig.update_layout(mapbox_style='open-street-map')
    tab3_fig.update_traces(marker=dict(opacity=0.8))
    tab3_fig.update_layout(legend=dict(x=0, y=1), margin=dict(l=50, r=50, t=50, b=50))
    tab3_fig.update_layout(mapbox=dict(center=dict(lat=tab3_filtered_data['latitude'].mean(), lon=tab3_filtered_data['longitude'].mean()), zoom=4))
    tab3_fig.update_layout(title='Methane emissions in the United States, 2019')

    return tab3_fig




@app.callback(Output('tab4-plot', 'figure'),[Input('death-type-dropdown', 'value')])
def update_tab4_plot(death_type):
    if death_type is None:
        tab4_df_filtered = tab4_df[tab4_df['ID'] == 'methane']

    else:
        tab4_df_filtered = tab4_df[tab4_df['ID'] == death_type]

    # Group the data by Year and Month, and calculate the total deaths for each combination
    tab4_df_grouped = tab4_df_filtered.groupby(['Year', 'Month'])['Deaths'].sum().reset_index()

    # Define the desired order of months
    month_order = ['Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'Jun.', 'Jul.', 'Aug.', 'Sep.', 'Oct.', 'Nov.', 'Dec.']

    # Convert the 'Month' column to categorical with the desired order
    tab4_df_grouped['Month'] = pd.Categorical(tab4_df_grouped['Month'], categories=month_order, ordered=True)

    # Sort the data by Year and Month
    tab4_df_grouped = tab4_df_grouped.sort_values(['Year', 'Month'])

    # Create the x-axis tick labels as month and year combinations
    x_ticks = [f'{month} {int(year)}' for year, month in zip(tab4_df_grouped['Year'], tab4_df_grouped['Month'])]

    # Create the hovertemplate with only the month, year, and number of deaths
    hovertemplate = 'Year: %{x}<br>Month: %{text}<br>Number of Deaths: %{y}'

    # Get the viridis color scale
    viridis_colors = colors.sequential.Viridis

    # Create the line plot using Plotly
    tab4_fig = go.Figure()
    tab4_fig.add_trace(go.Scatter(x=x_ticks, y=tab4_df_grouped['Deaths'],
                            mode='lines+markers', hovertemplate=hovertemplate,
                            line={'color': viridis_colors[0]},
                            text=tab4_df_grouped['Month']))  # Use the Month column for hover text

    # Set the plot title and labels
    tab4_fig.update_layout(
        #title=f'Trend in Number of Deaths ({desired_id.capitalize()}-related) Over Time',
        title=f'Number of Deaths Over Time by Cause',
        xaxis_title='Year',
        yaxis_title='Number of Deaths'
    )

    tab4_fig.update_xaxes(
        tickmode='array',
        tickvals=[idx for idx, month in enumerate(tab4_df_grouped['Month']) if month == 'Jan.'],
        ticktext=[str(int(year)) for year, month in zip(tab4_df_grouped['Year'], tab4_df_grouped['Month']) if month == 'Jan.'],
        tickformat='.0f'
    )

    # Remove the trace name from the legend
    tab4_fig.update_traces(name='')  

    return tab4_fig 




# Dash callback
@app.callback(dash.dependencies.Output('result-output', 'children'),[dash.dependencies.Input('location-input', 'value')])
def update_output(value):
    if value:
        # calling the Nominatim tool
        loc = Nominatim(user_agent="GetLoc")
        
        # entering the location name
        getLoc = loc.geocode(value, timeout=5)

        target_address = getLoc.address
        target_lon = getLoc.longitude
        target_lat = getLoc.latitude

        # Function to calculate distance between two points
        def calculate_distance(lon1, lat1, lon2, lat2):
            point1 = (lat1, lon1)
            point2 = (lat2, lon2)
            distance = geodesic(point1, point2).miles
            return distance

        # Calculate distances between target point and all points in the data frame
        distances = df_search.apply(lambda row: calculate_distance(target_lon, target_lat, row['longitude'], row['latitude']), axis=1)

        # Find the index of the closest point
        closest_index = distances.idxmin()

        # Retrieve the closest matching point
        closest_point = df_search.loc[closest_index]
        #closest_point['latitude'] = closest_point['latitude'].round(2)
        #closest_point['longitude'] = closest_point['longitude'].round(2)
        #closest_point['ch4'] = closest_point['ch4'].round(2)


        # Return the result
        return html.Div([
            html.H3('Target Address: {}'.format(target_address)),
            html.H4('Closest Point: {}'.format(closest_point))
        ])

    return ''







if __name__ == '__main__':
    app.run_server(host='localhost',port=8005)







# z1, z2, z3 = np.random.random((3, 7, 7))

# customdata = np.dstack((z2, z3))
# mycustomdata = np.dstack((hospitals["company_name"], hospitals["number_of_employees"]))
# mycustomdata = mycustomdata.T.tolist()



# mycustomdata = np.dstack((hospitals["company_name"], hospitals["phone_number"], hospitals["number_of_employees"], hospitals["previous_leaks_n"], hospitals["fossil_fuel_type"], hospitals["number_of_beds"])).T.tolist(),






























