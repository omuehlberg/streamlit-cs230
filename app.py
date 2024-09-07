"""Name: Liv Muehlberg
CS230-1
Data: Rest Areas in California
Description:
This program uses the "Rest Areas in California" data set, and allows users to interact and analyze the data. You can measure the distance between stops, search for amenities, and visualize the routes by city and route. 
This program also uses visual tools such as images, maps, and graphs to give users a more in depth analysis of Rest Stops in California. 
"""
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import math
import altair as alt


with open('requirements.txt', 'w') as file:
    file.write('streamlit\nnumpy\npandas\nmatplotlib\naltair\n')

Rest_Areas = 'Rest_Areas.csv'
Rest_AreasPath = os.path.abspath(Rest_Areas)
print(Rest_AreasPath)

App = 'app.py'
app_path = os.path.abspath(App)
print(app_path)

csv_file_path = 'Rest_Areas.csv' #affirming the path
amenities = ['RESTROOM', 'WATER', 'PICNICTAB', 'PHONE', 'HANDICAP', 'RV_STATION', 'VENDING', 'PET_AREA'] # storing data catagories in list 'amenities'


def top():
    st.title('Rest Stops in California') # title of my streamlit 

    st.caption("Created by Liv Muehlberg for Professor Babaian's CS230 section") # caption for credit
    
def image():
    image_url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/California_state_highways.svg/600px-California_state_highways.svg.png'
    st.image(image_url, caption='California Routes. Photo via Wikipedia: State highways in California', use_column_width=True)


def load_data(file_path):
    if os.path.exists(file_path):
        data = pd.read_csv(file_path) # loading data from CSV into data variable
        return data
    else:
        st.error(f'File not found: {file_path}') # error pathway if no data
        return None

def equation(coord1, coord2):
    lat1, lon1 = coord1 # first rest stop
    lat2, lon2 = coord2 # second rest stop
    euclidean_distance = ((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2) ** 0.5 # equation to find the distance between two points
    return euclidean_distance


def conversion(coord1, coord2, unit='miles'):
    lat1, lon1 = coord1 # first point
    lat2, lon2 = coord2 # second point
    
    latitude_miles = 69 * (lat2 - lat1) # turning latitude differences into miles
    
    avg_lat = (lat1 + lat2) /2
    avg_lat_radians = math.radians(avg_lat)
    longitude_miles = 69 * math.cos(avg_lat_radians) * (lon2 - lon1) # convert longitude points into miles
    
    miles = (latitude_miles ** 2 + longitude_miles ** 2) ** 0.5 # pythagorean theorem to determine direct distance
    if unit == 'km':
        miles *= 1.60934 # miles is default value, so convert if needed
    
    return latitude_miles, longitude_miles, miles


csv_file_path = 'Rest_Areas.csv' #reaffirming the path
data = load_data(csv_file_path)

def query1(data):
    st.header('Rest Stop Distance Calculator') # header for query1
    if {'MAP_LABEL_NAME', 'LATITUDE', 'LONGITUDE'}.issubset(data.columns): # finding the column names in the CSV file
        rest_stops = data.set_index('MAP_LABEL_NAME')[['LATITUDE', 'LONGITUDE']].T.to_dict('list') # creating list
        rest_stop1 = st.selectbox('Select the first rest stop:', list(rest_stops.keys())) # adding to list
        rest_stop2 = st.selectbox('Select the second rest stop:', list(rest_stops.keys())) # adding to list

        coord1 = rest_stops[rest_stop1] 
        coord2 = rest_stops[rest_stop2]
            
        if st.button('Calculate Distance'): # button to generate, conditional
            if rest_stop1 != rest_stop2: # rest stops cannot be the same
                latitude_miles, longitude_miles, miles = conversion(coord1, coord2)
                st.write(f'The distance between {rest_stop1} and {rest_stop2} is about')
                st.write(f'- Latitude Difference: {latitude_miles:.2f} miles')
                st.write(f'- Longitude Difference: {longitude_miles:.2f} miles')
                st.write(f'- Actual Distance: {miles:.2f} miles')
                distance = equation(coord1, coord2)
                st.write(f'The distance between {rest_stop1} and {rest_stop2} is approximately {miles:.2f}, or {distance: .2f}, units, according to the Euclidean Distance Theorem.')
                
                map_data = pd.DataFrame([coord1, coord2], columns=['LATITUDE', 'LONGITUDE']) # converts two points to be used in the map
                st.map(map_data.rename(columns={'LATITUDE': 'lat', 'LONGITUDE': 'lon'})) # create a map of specified locations using X point (lat) and Y point (lon) to graph them

            else:
                st.write('Please select two different rest stops.') # error pathway
    else:
        st.write('The dataset is missing columns.') # error pathway
        

city_names = data['CITY'].unique() # eliminates duplicates

def query2(data):
    st.header('Amenities Search') # header for query 2
    
    amenities = ['RESTROOM', 'WATER', 'PICNICTAB', 'PHONE', 'HANDICAP', 'RV_STATION', 'VENDING', 'PET_AREA'] # storing data catagories in list 'amenities'

    selected_amenities = st.multiselect("Please select the amenities you are looking for:", amenities) # multiselect streamlit function
    

    if st.button("Generate Table!"): # streamlit button
        filtered_data = data.copy() # copy of data, using user filters
    
        if selected_amenities: # conditional
            for amenity in selected_amenities: # selecting certain items in list
                filtered_data = filtered_data[filtered_data[amenity] == 'Yes'] # for the amenities in data that are selected, with the answer Yes, rewrite the filtered_data varible to display
    
        columns_displayed = ['MAP_LABEL_NAME', 'CITY', 'X', 'Y', 'LATITUDE', 'LONGITUDE', 'ROUTE'] + amenities # tells python/streamlit which data catagories we are putting in our new list
        displayed_data = filtered_data[columns_displayed]  # selecting columns from list
        
        st.write('Here are the Rest Stops that have the amenities searched for:')
        st.table(filtered_data[['MAP_LABEL_NAME', 'CITY', 'ROUTE', ] + selected_amenities]) # display the columns in list 'displayed' plus the ones selected by user
    
        st.header('Map of Rest Stops with Selected Amenities:')
        if len(displayed_data) > 0: # ensuring there is data
            st.map(displayed_data.rename(columns={'X': 'lon', 'Y': 'lat'})) # create a map of specified locations using X point (lat) and Y point (lon) to graph them
        else: # error pathways
            st.write("No rest stops match your search.")
        st.caption("Some rest stops are close together, please zoom in for a more accurate depiction. Darker red indicates two or more rest stops.") # note for user
    

def query3(data):
    st.header('Rest Stops Distribution by City') # title of query3
    
    city_names = data['CITY'].unique() # reaffirming no duplicates in the data names
    
    selected_cities = st.multiselect('Select cities to filter:', city_names) # streamlit multiselect function
    st.caption("Or select 'Generate Chart!' to see All Cities") # note for user: multiselect is optional
    
    if st.button("Generate Chart!"): # streamlit button to display data
        filtered_data = data[data['CITY'].isin(selected_cities)] if selected_cities else data # counts occurrances and prep data, list comp.
    
        city_dist = filtered_data['CITY'].value_counts().reset_index() # counts number of each city and resets the data frame to show the cities and counts
        city_dist.columns = ['CITY', 'Count'] # organize city_dist data into columns
    
        st.bar_chart(city_dist.set_index('CITY')) # create a bar chart using city_dist data


def query4(data):
    st.header('Rest Stops by Route Number') # title for query 4
    
    csv_file_path = 'Rest_Areas.csv'
    data = load_data(csv_file_path)
    
    if 'ROUTE' not in data.columns: # error pathway if there is no data
        st.write("No route data found.")
        return

    routes = sorted(data['ROUTE']) # sorting the route data
    
    if not routes: # error pathway if no route data in file
        st.write("No route data found.")
        return
    
    user_route = st.slider('Select a route number', min_value=min(routes), max_value=max(routes), step = 1) # streamlit slider for user entry
    sorting = st.selectbox('Sort by:', ['MAP_LABEL_NAME', 'CITY']) # selectbox streamlit function allowing user to sort by map name or city name
    
    if st.button("Generate Rest Stops Along Inputed Route!"): # streamlit button to generate data
        filtered_data = data[data['ROUTE'] == user_route] # using user inputed number to generate the route data in the variable filtered_data
            
        if filtered_data.empty: # error pathway if user selects a number not associated with routes
            unique_routes = sorted(set(routes))
            st.write("No rest stops along selected route.\n\nPossible routes are:" + ", ".join(map(str, unique_routes)))
        else:
            st.write(f'Rest Stops along {user_route}:') # displaying users selected route
            
            filtered_data = filtered_data.sort_values(by=sorting, ascending=True) # filtering and sorting the filtered_data 
                
            st.table(filtered_data[['MAP_LABEL_NAME', 'CITY', 'LATITUDE', 'LONGITUDE', 'ROUTE']]) # streamlit table displaying user data
            
            route_dist = data['ROUTE'].value_counts().sort_index().reset_index() # counts route occurances, sorts them and sets the data frame to the selected data
            route_dist.columns = ['ROUTE', 'Number of Stops']
            st.header("Distribution of Rest Stops per Route") # graph title
            st.scatter_chart(route_dist.set_index('ROUTE')) # streamlit chart showing distribution of all available routes
            st.caption("Highlight over points to see specifics. The routes are on the horizontal axis, amounts on vertical.") # note for user

def image2():
    image_url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/01/Flag_of_California.svg/510px-Flag_of_California.svg.png'
    st.image(image_url, caption='California Flag. Image via Wikipedia: Flag of California', use_column_width=True)


def main():
    top()
    image()
    
    data = load_data(csv_file_path)
    if data is not None:
        query1(data)
        query2(data)
        query3(data)
        query4(data)   

    image2()
    

if __name__ == '__main__':
    main()
