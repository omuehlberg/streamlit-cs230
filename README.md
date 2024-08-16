IMPORTING 

First in my code, I imported all necessary components, such as streamlit, math and pandas. I have in my comments the code to find the pathway to my needed documents, and I have the CSV path and the amenities at the top, as those are used in many of the queries. 

 

HEADER 

In the top() defined function, I added a header and a caption to give credit. The next component is an image of the California highways, to add to the visual aspect of my project. 

 

DATA LOADING 

‘load_data’ loads the csv file with the rest stop data and has an option to print if the pathway for the file is not found. This is referenced in each query, to access the ‘data’. 

 

QUERY1 

For Query 1, I chose to build a function that calculates the distance between two selected rest stops. The only location data given in the CSV file is latitude and longitude, so I had to do some research to figure out the exact conversion. The ‘equation’ and ‘conversion’ functions calculate the distance using the Euclidean distance theorem and the Pythagorean theorem. There is also code to convert the units into the default units of miles.  

 

Query 1 has users select the two rest stops and a button to generate the distance between them. Rest Stops are not allowed to be the same, and there is an error pathway if the two are the same. The output tells the user the distance difference between the points in terms of latitude and longitude miles, Euclidean distance units, and finally the direct distance between the two points. Then, a map is produced showing the two stops selected, to give the user a visual.  

 

Next, I defined the city names, as I will work with them in the next queries. The unique addition helps to reduce duplication in user selection.  

 ]

QUERY 2

For query 2, I chose to do an output of rest stops based on the user’s desired amenities. The type of amenity is taken from the CSV file, including ‘BATHROOM’ and ‘PHONE’. The users are directed to select the amenities they are searching for from a multi-select box. A button was created to allow users to generate the table, instead of it being available at the beginning and crowding the page. Once the button is pressed, any rest stops with the selected amenities are shown in a table, and the map produces the location of rest stops with the selected amenities. I added a caption, as there were some rest stops close together, and the data appears to be misleading. In the code, I added a path if there is no data, or the multi-select box is left empty, as needed when you use a define function.  

 

QUERY 3 

For Query 3, I wanted to use a chart element to show the distribution of the rest stops in each city. The code is written to use list comprehension, by creating a filtered list and using the if/else build to give an option to use the original data if the user would like to see all available cities. They can generate the original and complete data by clicking the ‘Generate Chart!’ button to see all cities. They can also highlight over the chart, to get more information. 

 

QUERY 4 

Finally, the last query allows the user to view rest stops along a specific route. I wanted to utilize the slide feature, so I put the smallest and largest route numbers as the minimum and maximum. If the user selects a number not associated with a route, there is an error path in the code, and they are given a list and asked to regenerate. In the event they pick a route number, they are given a choice to sort the data in the generated table alphabetically, either by city or by rest stop name. There is also a scatter plot that helps users to visualize the distribution of rest stops by route. 

 

Finally, I inserted another image, this time of the California flag. This adds some color and is on theme with the site.  

 

MAIN 

At the bottom of the code, the defined functions run under the main() function. The top, image 1 and image 2 feature should run regardless of the code, but if there is no data query1-4 do not run. If there is data, they should run within main.  
