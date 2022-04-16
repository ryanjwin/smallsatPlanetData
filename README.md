# Downloading data using Planet Data API and Order API 

> Ryan Winkelman

> Undergraduate Student at the University of Texas at El Paso

> Last Updated April 16, 2022

## Getting started
The code uses Python3 and the following libraries:
 - os
 - json
 - requests
 - pandas
 - pathlib
 - dotenv
 
If a library is not installed it can be installed running the following command on the terminal:
 
`pip3 install replace-with-library-name`

A Planet API key is required as well. One is included with a Planet Account. And can be found by going to account settings.  Seen below

![Location of Planet API Key](https://github.com/ryanjwin/smallsatPlanetData/blob/main/images/Screen%20Shot%202022-04-16%20at%2012.18.04%20PM.png?raw=True)


Save the Planet API Key as an environment variable. To do so create a .env in the project directory and enter the following

`PLANET_API_KEY=replace-with-api-key`

After initial setup, coordinates of regions of interest must be aquired. To aquire these a free online tool, [geojson](http://geojson.io), is available. 

Using this tool, navigate to the region of interest and select the polygon tool to began drawing a polygon overlay on the image.

![Showing polygon tool on geojson](https://github.com/ryanjwin/smallsatPlanetData/blob/main/images/Screen%20Shot%202022-04-16%20at%201.08.41%20PM.png?raw=True)

After drawing the region, copy the json on the right from the first opening curly braces after “geometry” to the first closing curly brace.

![Using polygon 1](https://github.com/ryanjwin/smallsatPlanetData/blob/main/images/Screen%20Shot%202022-04-16%20at%201.14.46%20PM.png?raw=True)

![Using polygon 2](https://github.com/ryanjwin/smallsatPlanetData/blob/main/images/Screen%20Shot%202022-04-16%20at%201.14.52%20PM.png?raw=True)

Next, use the csv file titled "locations.csv" to enter in the regions of interest for the order, each region will be a seperate order.

First, give a proper name to the region, include the year that you are seeking data from.

Paste this json into the csv file under “Polygon Coordinates”.
![CSV polygon](https://github.com/ryanjwin/smallsatPlanetData/blob/main/images/Screen%20Shot%202022-04-16%20at%201.14.59%20PM.png?raw=True)

Modify the json in the Dates column of the csv. Putting the beginning date following the “gte” and the end date following the “lte”. To avoid any issues, it is best to use the first of every month instead of the last day of the month.


![CSV dates](https://github.com/ryanjwin/smallsatPlanetData/blob/main/images/Screen%20Shot%202022-04-16%20at%201.15.04%20PM.png?raw=True)

Modify the json in the Code Coverage column. Replacing the number after “lte” with the desired cloud coverage

![CSV clouds](https://github.com/ryanjwin/smallsatPlanetData/blob/main/images/Screen%20Shot%202022-04-16%20at%201.15.11%20PM.png?raw=True)

Finally change the desired Item Type. In most cases it should be “PSScene”. Under asset type enter all the assets that you would like to select **separated by one space**. [Here](https://developers.planet.com/docs/data/psscene/) is a list of all available asset types for PSScene.


![CSV asset type](https://github.com/ryanjwin/smallsatPlanetData/blob/main/images/Screen%20Shot%202022-04-16%20at%201.15.17%20PM.png?raw=True)



# Rest of documentation pending finalization of notebook
