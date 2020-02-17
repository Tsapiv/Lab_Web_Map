Web Film Map
==========================
Aim of this project is to let user see on the map places, near given location, where famous movies were filmed.
## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.
### Prerequisites
That're things you need to install to get started

    python -m pip install folium
    python -m pip install geopy
    python -m pip install pycountry
### Installing

    $ git clone https://github.com/Tsapiv/Lab_Web_Map.git
### Running
`main.py` is a module to run. Once you run it, you'll get request like this `Please enter a year you would like to have a map for:`
It's better to enter year closer to the current one because there're more data available. For now let it be `1995`.
The next request `Please enter your location (format: lat, long):` asks you enter coordinates.
For now, let it be `31, -95`. It is somewhere in USA. If everything went well, in this particular case your console would look like this:

    Please enter a year you would like to have a map for: 1995
    Please enter your location (format: lat, long): 31, -95
    Map is generating...
    Please wait...
    Finished. Please have look at the map 1995_movies_map.html
So, what you are left to do is to open `1995_movies_map.html` in your browser.
In this particular case, you must get something like this:
***
![screenshot of sample](https://github.com/Tsapiv/Lab_Web_Map/blob/master/examples/map_example_1.png)
***
However, if your input is like this:

    Please enter a year you would like to have a map for: 2005
    Please enter your location (format: lat, long): 0, -160
    Invalid coordinates
(`0, -160` it is somewhere in Pacific ocean) You got nothing because
in the middle of the ocean were made no films.
And for the full picture:

    Please enter a year you would like to have a map for: 2010
    Please enter your location (format: lat, long): 49.83826, 24.02324
    Map is generating...
    Please wait...
    Finished. Please have look at the map 2010_movies_map.html
***
![screenshot of sample](https://github.com/Tsapiv/Lab_Web_Map/blob/master/examples/map_example_2.png)
***
### Contributing
* Sometimes, there can occur some issues with `geopy`, just ignore it.
* The third layer of this map color countries depending on their area. The country of the territory of which the user-specified coordinates belong is highlighted with blue color.
### Authors
* Tsapiv Volodymyr

