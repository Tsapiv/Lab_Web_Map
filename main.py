import folium
import pycountry
from geopy.geocoders import Nominatim


def eval_closeness(dct1, dct2):
    """
    (dict) -> dict
    Return swapped dictionary of closeness
    where closeness is a key and film is value
    >>> eval_closeness({'Dallas, Texas, USA': 3, 'Texas, USA': 4,\
    'San Antonio, Texas, USA': 4,\
    'Houston, Texas, USA': 24}, {'Dallas, Texas, USA': 3, 'Texas, USA': 4,\
    'San Antonio, Texas, USA': 4, 'Houston, Texas, USA': 24})
    {'Dallas, Texas, USA': 1.0, 'Texas, USA': 1.0, 'San Antonio, \
Texas, USA': 1.0, 'Houston, Texas, USA': 1.0}
    """
    new_dct = {}
    for key in dct1:
        new_dct[key] = dct1[key] / dct2[key]
    return new_dct


def matcher(country):
    """
    (str) -> str
    Return valid names for some countries
    >>> matcher(['Shapikhy', ' Openky', ' Kozelets Raion',\
    ' Chernihiv Oblast', ' 17052', ' Ukraine'])
    ['Shapikhy', 'Openky', 'Kozelets Raion', 'Chernihiv Oblast', '17052', 'Ukraine']
    >>> matcher(['Wilson County', ' Kansas', ' United States of America'])
    ['Wilson County', 'Kansas', 'USA, US']
    """
    corrector = {"America": "USA, US", "United Kingdom": "UK",
                 "United States of America": "USA, US"}
    country = list(map(lambda x: x.strip(), country))
    country[-1] = corrector.get(country[-1], country[-1])
    return country


def get_country(user_loc):
    """
    (str) -> str
    Return name of the country with given coordinates
    >>> get_country("55, 34")
    Location(66Н-0210, Большое Староселье, Семлево, Vyazemsky District, Smolensk Oblast, \
Central Federal District, Russia, (54.99537433463528, 33.99718116940419, 0.0))
    >>> get_country("26, 4")
    Location(In Amguel, de Tamanrasset District, Tamanrasset, Algeria, \
(24.9241475, 3.5840943785412014, 0.0))
    """
    geolocation = Nominatim(user_agent="web_map")
    return geolocation.reverse(user_loc, language="en")


def reader(year, country):
    """
    (str) - > dict, dict
    Return dictionary where location are keys and films are values
    and another dictionary which represent closeness
    """
    location_dict = {}
    closeness_dict = {}
    count_dict = {}
    with open("locations.list", "r", encoding="utf-8", errors="ignore") as file:
        temp = file.readline()
        while not temp.startswith("="):
            temp = file.readline()
        line = file.readline()
        while not line.startswith('-'):
            clear_line = line.strip().split("\t")
            try:
                film_and_year = clear_line[0]
                loc = -2 if clear_line[-1].startswith("(") else -1
                separator = film_and_year.find("(")
                film, release, location = film_and_year[:separator].strip(), \
                                          int(film_and_year[separator + 1: separator + 5]), \
                                          clear_line[loc]
                loc_line = list(map(lambda x: x.strip(), location.split(",")))
                closeness = len(set(country) & set(loc_line))
                if release == year and closeness != 0:
                    temp_film_set = location_dict.get(location, set())
                    temp_film_set.add(film)
                    location_dict[location] = temp_film_set
                    closeness_dict[location] = closeness_dict.get(location, 0) + closeness
                    count_dict[location] = count_dict.get(location, 0) + 1
            except:
                pass
            line = file.readline()
    return location_dict, closeness_dict, count_dict


def find_location(location):
    """
    (str) -> tuple
    Return longitude and latitude оf the place where the films were shot
    >>> find_location("Lviv")
    (49.841952, 24.0315921)
    >>> find_location("London")
    (51.5073219, -0.1276474)
    """
    geolocation = Nominatim(user_agent="nagibator")
    geo_loc = geolocation.geocode(location)
    if geo_loc is None:
        return 0, 0
    return geo_loc.latitude, geo_loc.longitude


def find_closest(dict_loc):
    """
    (dict) -> dict
    Return 10 or less closest locations
    >>> find_closest({"a": 4, "b": 3, "c": 2, "d": 78, "s": 23, "as": 23,\
     "gh": 21, "jh": 45, "f": 11, "r": 8, "df": 7})
    {'a': 4, 'b': 3, 'd': 78, 's': 23, 'as': 23, 'gh': 21, \
'jh': 45, 'f': 11, 'r': 8, 'df': 7}
    >>> find_closest({"c": 2, "d": 78, "s": 23, "as": 23, "gh": 21,\
     "jh": 45, "f": 11, "r": 8, "df": 7})
    {'c': 2, 'd': 78, 's': 23, 'as': 23, 'gh': 21, \
'jh': 45, 'f': 11, 'r': 8, 'df': 7}
    """
    new_dict = {}
    if len(dict_loc) <= 10:
        return dict_loc
    check_list = sorted(dict_loc.values())[-10:]
    i = 0
    for key in dict_loc:
        if dict_loc[key] in check_list:
            new_dict[key] = dict_loc[key]
            if i == 10:
                break
            i += 1
    return new_dict


def circle(amount):
    """
    (int) -> tuple
    Return radius and color of circle for
    given amount of the films
    >>> circle(5)
    (25, 'blue')
    >>> circle(300)
    (50, 'red')
    """
    radius = amount * 5 if amount * 5 <= 50 else 50
    if amount <= 2:
        color = "green"
    elif amount <= 5:
        color = "blue"
    elif amount <= 8:
        color = "orange"
    else:
        color = "red"
    return radius, color


def determinate_country(country):
    """
    (str) -> str
    Return name of the country in ISO-2 format
    >>> determinate_country("Ukraine")
    'UG'
    >>> determinate_country("England")
    'BD'
    """
    country_code = pycountry.countries.search_fuzzy(country[-1])[0].alpha_2
    return country_code


def input_checker(year, coordinates):
    """
    (str) -> boolean
    Return whether user input is valid
    >>> input_checker("2003", "4987, 34")
    Try enter real coordinates.
    False
    >>> input_checker("200jfh3", "87, 34")
    False
    >>> input_checker("2003", "87, 34")
    True
    """
    try:
        if int(year) not in range(1900, 2020):
            print("Try enter year between 1900 and 2020.")
            return False
        lat, lng = coordinates.split(",")
        if float(lat) > 180 or float(lat) < -180 \
                or float(lng) > 180 or float(lng) < -180:
            print("Try enter real coordinates.")
            return False
    except:
        return False
    return True


def build_map(user_loc, position_dict, country, year):
    """
    (tuple, dict) -> ()
    Create a map with marked places on it where movies
    of a particular year were filmed
    Country that is painted in blue is the country where coordinates given by user are
    blue, other countries are painted in colors depending on their area
    """
    web_map = folium.Map(location=[user_loc[0], user_loc[1]],
                         zoom_start=7)
    fg_films = folium.FeatureGroup(name="Places of glory")
    for position in position_dict:
        if position == (0, 0):
            continue
        text = '<br>'.join(list(position_dict[position])).strip('<br>')
        popup = folium.Popup(text, max_width=450)
        radius, color = circle(len(position_dict[position]))
        folium.CircleMarker(
            location=position,
            radius=radius,
            popup=popup,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.6
        ).add_to(fg_films)
    fg_area = folium.FeatureGroup(name="Area")
    user_country = determinate_country(country)
    fg_area.add_child(folium.GeoJson(data=open('world.json', 'r',
                                               encoding='utf-8-sig').read(),
                                     style_function=lambda x: {
                                         'fillOpacity': 0.5,
                                         'fillColor': '#54EFE1' if
                                                      x['properties']['ISO2'] == user_country
                                                      else 'green'
                                                      if x['properties']['AREA'] < 30000
                                                      else 'orange' if 30000 <= x['properties'][
                                                          'AREA'] < 100000
                                                      else 'red'}))
    web_map.add_child(fg_area)
    web_map.add_child(fg_films)
    web_map.add_child(folium.LayerControl())
    web_map.save("{}_movies_map.html".format(year))


def main():
    """
    () -> ()
    Calls functions to make web-map
    """
    year = input("Please enter a year you would like to have a map for: ")
    coordinates = input("Please enter your location (format: lat, long): ")
    if input_checker(year, coordinates):
        lat, lng = list(map(float, coordinates.split(",")))
        try:
            raw_country = str(get_country(coordinates)).split(",")
        except:
            print("Invalid coordinates")
            return
        print("Map is generating...\nPlease wait...")
        country = matcher(raw_country)
        year = int(year)
        location_dict, temp_dict, count_dict = reader(year, country)
        closeness_dict = eval_closeness(temp_dict, count_dict)
        list_of_closest_locations = find_closest(closeness_dict)
        list_of_films = [location_dict[loc] for loc in list_of_closest_locations]
        new_location_dict = dict(zip(list(map(find_location, list_of_closest_locations)),
                                     list_of_films))
        build_map((lat, lng), new_location_dict, raw_country, year)
        print("Finished. Please have look at the map {}_movies_map.html".format(year))
    else:
        print("Try again!")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    main()
