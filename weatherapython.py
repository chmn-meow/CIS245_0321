# project req's
# must be viewed in a readable format
# Create a Python Application which asks the user for their zip code or city.
# Use the zip code or city name in order to obtain weather forecast data from: http://openweathermap.org/
# Display the weather forecast in a readable format to the user.
# Use comments within the application where appropriate in order to document what the program is doing.
# Use functions including a main function.
# Allow the user to run the program multiple times.
# Validate whether the user entered valid data. If valid data isn’t presented notify the user.
# Use the Requests library in order to request data from the webservice.
# Use Python 3.
# Use try blocks when establishing connections to the webservice.
# You must print a message to the user indicating whether or not the connection was successful.

# just some text...


# import requisite libraries
import os
import requests
import json
import time
from datetime import datetime

from dotenv import load_dotenv, find_dotenv

# load and define global constants
load_dotenv(find_dotenv())
API = str(os.environ.get("API"))


class Menu(object):
    def __init__(self, name, master_menu=dict):
        self.current = name
        self.master_menu = master_menu
        self.top = True
        self.treed = False
        self.tree_lvl = 0
        self.parent = None
        self.sub_parent = None
        self.curr_menu = self.master_menu[self.current]
        self.navigating = False
        self.end_program = False
        self.options = self.master_menu[self.current].keys()

    def navigate(self):
        # this is bread and butter of the menu system.  It all stems from here.
        self.navigating = True
        self.build_menu()
        selection = input("Your selection?\n> ")
        return self.select(selection)

    def select(self, selection):
        # handler for menu selection
        try:
            sel = int(selection)
            itr = 0
            if sel == itr or itr < 0:
                raise ValueError
            else:
                for key, value in self.curr_menu.items():
                    itr += 1
                    if itr == sel:
                        # if it's a dictionary, it's a menu
                        if isinstance(value, dict):
                            if self.top:
                                self.top = False
                                self.treed = True
                                self.tree_lvl = 1
                                self.parent = self.current
                                self.current = key
                                self.curr_menu = value
                            elif not self.top:
                                self.tree_lvl = 2
                                self.sub_parent = self.current
                                self.current = key
                                self.curr_menu = value
                            return self.navigate()
                        # if it's a string, it's a menu command
                        elif isinstance(value, str):
                            if value == "upone" or value == "exit":
                                if value == "upone":
                                    if self.tree_lvl == 1:
                                        self.top = True
                                        self.treed = False
                                        self.tree_lvl = 0
                                        self.current = self.parent
                                        self.parent = None
                                        self.curr_menu = self.master_menu[self.current]
                                    elif self.tree_lvl == 2:
                                        self.tree_lvl = 1
                                        self.current = self.sub_parent
                                        self.sub_parent = None
                                        self.curr_menu = self.master_menu[self.parent][
                                            self.current
                                        ]
                                    return self.navigate()
                                elif value == "exit":
                                    return self.exit_program()
                        # if it's a callable, it's a function
                        elif callable(value):
                            return value()
                    elif itr > len(self.curr_menu.keys()):
                        raise ValueError
                    else:
                        pass
        except ValueError:
            print(f"{selection} is not a number in the sequence! Try again.")
            return self.navigate()
        except TypeError:
            print(
                f"Your selection of {selection} was not recognized. Please try again."
            )
            return self.navigate()

    def build_menu(self):
        # menu building handler
        print(f"{self.current} Menu:")
        if not self.treed:
            mn = 1
            for option in self.master_menu[self.current].keys():
                print(f"[{mn}] : {option}")
                mn += 1
            return
        elif self.treed:
            if self.tree_lvl == 1:
                mn = 1
                for option in self.master_menu[self.parent].keys():
                    print(f"[{mn}] : {option}")
                    mn += 1
                    if option == self.current:
                        smn = 1
                        for s_option in self.master_menu[self.parent][
                            self.current
                        ].keys():
                            print(f"  ^-> [{smn}] : {s_option}")
                            smn += 1
                        return
            elif self.tree_lvl == 2:
                mn = 1
                for option in self.master_menu[self.parent].keys():
                    print(f"[{mn}] : {option}")
                    mn += 1
                    if option == self.sub_parent:
                        smn = 1
                        for s_option in self.master_menu[self.parent][
                            self.sub_parent
                        ].keys():
                            print(f"  ^-> [{smn}] : {s_option}")
                            smn += 1
                            if s_option == self.current:
                                ssmn = 1
                                for ss_option in self.master_menu[self.parent][
                                    self.sub_parent
                                ][self.current].keys():
                                    print(f"    ^-----> [{ssmn}] : {ss_option}")
                                    ssmn += 1
                                return

    def exit_program(self):
        # exit program handler
        msg = "Are you sure you'd like to exit the program?"
        if get_yn(msg):
            self.navigating = False
            self.end_program = True
            print("Exiting")
            exit()
        else:
            return enter()


class Locale(object):
    # creating a locale object to store information
    city_name = str(os.environ.get("CITYNAME"))
    city_id = int(os.environ.get("CITYID"))
    gust = None
    zip_code = None
    search = False
    s_type = None
    query = None

    def __init__(self):
        data = self.scrape()
        self.update(data)

    def update(self, js):
        # takes the unparsed scrape and fits it to our object
        if not js:
            print(f"And more errors.  Connect to the internet, maybe?")
        else:
            for key, value in js.items():
                if isinstance(value, dict):
                    if key == "coord":
                        for k, v in value.items():
                            if k == "lon":
                                self.long = v
                            elif k == "lat":
                                self.lat = v
                            else:
                                pass
                        if self.long > 0:
                            lon = "E"
                        else:
                            lon = "W"
                        if self.lat > 0:
                            lat = "N"
                        else:
                            lat = "S"
                        self.coord = f"{self.lat} {lat}, {self.long} {lon}"
                    elif key == "main":
                        for k, v in value.items():
                            if k == "temp":
                                self.temp = v
                            elif k == "feels_like":
                                self.feels = v
                            elif k == "temp_min":
                                self.min = v
                            elif k == "temp_max":
                                self.max = v
                            elif k == "pressure":
                                self.pressure = v
                            elif k == "humidity":
                                self.humidity = v
                            else:
                                pass
                    elif key == "wind":
                        for k, v in value.items():
                            if k == "speed":
                                self.wind_speed = v
                            elif k == "gust":
                                self.gust = v
                            elif k == "deg":
                                if v > 348.75 or v <= 11.25:
                                    self.wind_dir = "Northerly"
                                elif v > 11.25 and v <= 33.75:
                                    self.wind_dir = "North-North-Easterly"
                                elif v > 33.75 and v <= 56.25:
                                    self.wind_dir = "North-Easterly"
                                elif v > 56.25 and v <= 78.75:
                                    self.wind_dir = "East-North-Easterly"
                                elif v > 78.75 and v <= 101.25:
                                    self.wind_dir = "Easterly"
                                elif v > 101.25 and v <= 123.75:
                                    self.wind_dir = "East-South-Easterly"
                                elif v > 123.75 and v <= 146.25:
                                    self.wind_dir = "South-Easterly"
                                elif v > 146.25 and v <= 168.75:
                                    self.wind_dir = "South-South-Easterly"
                                elif v > 168.75 and v <= 191.25:
                                    self.wind_dir = "Southerly"
                                elif v > 191.25 and v <= 213.75:
                                    self.wind_dir = "South-South-Westerly"
                                elif v > 213.75 and v <= 236.25:
                                    self.wind_dir = "South-Westerly"
                                elif v > 236.25 and v <= 258.75:
                                    self.wind_dir = "West-South-Westerly"
                                elif v > 258.75 and v <= 281.25:
                                    self.wind_dir = "Westerly"
                                elif v > 281.25 and v <= 303.75:
                                    self.wind_dir = "West-North-Westerly"
                                elif v > 303.75 and v <= 326.25:
                                    self.wind_dir = "North-Westerly"
                                elif v > 326.25 and v <= 348.75:
                                    self.wind_dir = "North-West-Northerly"
                                else:
                                    self.wind_dir = "That-way-ish-ly"
                            else:
                                pass
                    elif key == "clouds":
                        self.cloudiness = value["all"]
                    elif key == "rain":
                        self.rain = value
                    elif key == "snow":
                        self.snow = value
                    elif key == "sys":
                        self.concode = value["country"]
                        utc_sunrise = value["sunrise"]
                        utc_sunset = value["sunset"]
                    else:
                        pass
                elif isinstance(value, list):
                    if key == "weather":
                        iter = 1
                        self.weather = {}
                        for dic in value:
                            self.weather[iter] = {}
                            for k, v in dic.items():
                                self.weather[iter][k] = v
                            iter += 1
                    else:
                        pass
                elif isinstance(value, str):
                    if key == "base":
                        pass
                    elif key == "name":
                        self.city_name = value
                    else:
                        pass
                elif isinstance(value, int):
                    if key == "visibility":
                        self.visibility = value // 1000
                    elif key == "dt":
                        utc_call = value
                    elif key == "timezone":
                        timezone = value
                    elif key == "id":
                        self.city_id = value
                    else:
                        pass
                else:
                    pass
            ts = utc_call + timezone
            s = utc_sunrise + timezone
            ss = utc_sunset + timezone
            self.last_called = datetime.utcfromtimestamp(ts).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            self.sunrise = datetime.utcfromtimestamp(s).strftime("%I:%M %p")
            self.sunset = datetime.utcfromtimestamp(ss).strftime("%I:%M %p")
            self.date, self.time = get_time(timezone)

    def display_location(self):
        # this will display currently active location's data
        print(f"Currently, our saved city is {self.city_name}.")
        time.sleep(0.3)
        print(f"The city of {self.city_name} is coded as Id#: {self.city_id}.")
        time.sleep(0.3)
        print(f"The lat-long is {self.coord}, which is in the {self.concode}.")
        time.sleep(0.3)
        enter()

    def quick_weather(self):
        # this will be the quick weather details printer
        time.sleep(0.3)
        print(
            f"It is currently {self.weather[1]['description']} in the {self.city_name} area. It is {self.temp} degrees, feeling like an average {self.feels} degrees."
        )
        time.sleep(0.3)
        enter()

    def display_weather(self):
        # this will be the detailed weather printer
        time.sleep(0.3)
        print(f"It is {self.time} in {self.city_name} on {self.date}.\n")
        time.sleep(0.3)
        print(
            f"We have {self.weather[1]['description']} with a temperature of {self.temp} degrees, though it feels like {self.feels} degrees.\n"
        )
        time.sleep(0.3)
        print(f"The high for today is {self.max} with a low of {self.min} degrees.\n")
        time.sleep(0.3)
        print(
            f"Humidity is at {self.humidity}% with an atmospheric pressure of {self.pressure} hPa.\n"
        )
        time.sleep(0.3)
        if self.gust:
            gusts = f"Gusts are up to {self.gust} mpg."
        else:
            gusts = "There are no gusts at this hour."
        print(
            f"We have a {self.wind_dir} wind blowing at {self.wind_speed} mph. {gusts}\n"
        )
        time.sleep(0.3)
        print(
            f"Cloud cover is at {self.cloudiness}%, and visibility is pegged at approximately {self.visibility} km.\n"
        )
        time.sleep(0.3)
        print(
            f"Expected sunrise and sunset times today are {self.sunrise} and {self.sunset}, respectively.\n"
        )
        time.sleep(0.3)
        enter()

    def name_search(self):
        # named search handler.  This works just about as well as geocoord searching.  This is probably a little more accurate, but
        # both are quite valid search methods.
        msg = "Are you looking up a city in the US?"
        if get_yn(msg):

            city = ""
            while not city:
                city = input(werder("cin"))
            state = ""
            while len(state) > 2 or not state:
                state = input(werder("sin"))
            country = "us"

            query = f"{city.title()}, {state.upper()}, {country.upper()}"
            verify = get_yn(f"You said {query}, is that right?")

            if verify:
                self.search = True
                self.s_type = "name"
                self.query = query
                data = self.scrape()
                self.update(data)
                self.display_weather()
                self.search = False
            else:
                return
        else:
            city = ""
            while not city:
                city = input(werder("cin"))
            country = ""
            while len(country) > 2 or not country:
                country = input(werder("coin"))

            query = f"{city.title()}, {country.upper()}"
            verify = get_yn(f"You said {query}, is that right?")

            if verify:
                self.search = True
                self.s_type = "name"
                self.query = query
                data = self.scrape()
                self.update(data)
                self.display_weather()
                self.search = False
            else:
                return

    def cid_search(self):
        # city id # search handler thing.  This is the single most reliable search method, provided you know open weather's
        # city codes.  I should include that with a quick "inspect locale" feature/function...
        cid = ""
        while not cid:
            cid = input(werder("cid"))

        try:
            int(cid)
        except ValueError:
            print("Sorry, you didn't type only numbers for that.  Please try again!")
            return self.zip_search()
        query = f"{cid}"
        verify = get_yn(f"You said {query}, is that right?")
        if verify:
            self.search = True
            self.s_type = "id"
            self.query = query
            data = self.scrape()
            if not data:
                print("Huh, normally that works...")
                time.sleep(2)
                msg = "We can try a different code, if you'd like."
                if get_yn(msg):
                    time.sleep(1)
                    print("Ok, hang on.")
                    time.sleep(0.5)
                    return self.cid_search()
                else:
                    time.sleep(1)
                    print("Ok, I'll just send you back to the menu. Sorry.")
                    time.sleep(1)
                    return
            else:
                self.update(data)
                self.display_weather()
                self.search = False
        else:
            return

    def zip_search(self):
        # zip search handler
        # regardless of how I do it, even just using raw browser connection, I could not get a single city to pop using zip codes
        # I don't know if they just created an error during their last update, cause I do remember having done it when I first looked
        # at the API documentation...I don't remember what zip I used at that time, though.  Nothing, including ones I've found on
        # forums talking about this issue that users said worked for them, haven't worked for me.  Strange...will monitor

        print(
            "Quick disclaimer: Open Weather does not like to search by zip codes, for some reason.  I don't quite understand what their problem is, but there's only a few zip codes they like."
        )
        enter()
        msg = "Are you looking up a city in the US?"
        if get_yn(msg):
            czip = ""
            while not czip or len(czip) < 4:
                czip = input(werder("ciz"))
            country = "us"

            try:
                int(czip)
            except ValueError:
                print(
                    "Sorry, you didn't type only numbers for that.  Please try again!"
                )
                return self.zip_search()

            query = f"{czip}, {country.upper()}"
            verify = get_yn(f"You said {query}, is that right?")

            if verify:
                self.search = True
                self.s_type = "zip"
                self.query = query
                data = self.scrape()
                if not data:
                    print(
                        "Yea, sorry. Open Weather doesn't really like looking up by zip. If you have the city-id code or name, you could try that."
                    )
                    time.sleep(2)
                    msg = "We can try a different zip, if you'd like. Well?"
                    if get_yn(msg):
                        time.sleep(1)
                        print("Ok, hang on.")
                        time.sleep(0.5)
                        return self.zip_search()
                    else:
                        time.sleep(1)
                        print("Ok, I'll just send you back to the menu. Sorry.")
                        time.sleep(1)
                        return

                else:
                    self.update(data)
                    self.display_weather()
                    self.search = False
            else:
                return

    def geo_search(self):
        # geocoord search handler thing, works better than zip codes, for some reason
        lat = ""
        while not lat:
            lat = input("The Latitude?\n> ")
        lon = ""
        while not lon:
            lon = input("The Longitude?\n> ")

        try:
            float(lat)
            float(lon)
        except ValueError:
            print("Sorry, you didn't type only numbers for that.  Please try again!")
            return self.geo_search()
        query = f"{lat}, {lon}"
        verify = get_yn(f"You said {query}, is that right?")
        if verify:
            self.search = True
            self.s_type = "geo"
            self.query = [lat, lon]
            data = self.scrape()
            if not data:
                print("Huh, normally that works...")
                time.sleep(2)
                msg = "We can try a different coordinate, if you'd like."
                if get_yn(msg):
                    time.sleep(1)
                    print("Ok, hang on.")
                    time.sleep(0.5)
                    return self.geo_search()
                else:
                    time.sleep(1)
                    print("Ok, I'll just send you back to the menu. Sorry.")
                    time.sleep(1)
                    return
            else:
                self.update(data)
                self.display_weather()
                self.search = False
        else:
            return

    def scrape(self, att=1):
        # this will be the primary API actor
        attempt = att
        url = "https://api.openweathermap.org/data/2.5/weather"
        if self.search:
            if self.s_type == "name":
                parameters = {
                    "q": self.query,
                    "appid": API,
                    "units": "imperial",
                    "lang": "en",
                }
            elif self.s_type == "city_id":
                parameters = {
                    "id": self.query,
                    "appid": API,
                    "units": "imperial",
                    "lang": "en",
                }
            elif self.s_type == "zip":
                parameters = {
                    "zip": self.query,
                    "appid": API,
                    "units": "imperial",
                    "lang": "en",
                }
            elif self.s_type == "geo":
                parameters = {
                    "lat": self.query[0],
                    "lon": self.query[1],
                    "appid": API,
                    "units": "imperial",
                    "lang": "en",
                }
            else:
                parameters = {
                    "id": self.city_id,
                    "appid": API,
                    "units": "imperial",
                    "lang": "en",
                }
        else:
            parameters = {
                "id": self.city_id,
                "appid": API,
                "units": "imperial",
                "lang": "en",
            }
        if att < 3:
            try:
                r = requests.get(url, parameters)
                r.raise_for_status()
                while r.status_code == requests.codes.ok:  # pylint: disable=no-member
                    data = json.loads(r.text)
                    # for testing purposes, we will save these results to a file for now.
                    # comment before turning in...otherwise, it may spit an error at the prof
                    # with open("weather.json", "w") as f:
                    #    json.dump(data, f, indent=4)
                    break
                return data
            except requests.exceptions.HTTPError:
                # we're just going to use requests' prebuild exceptions to handle
                attempt += 1
                msg = f"Search was unsuccessful on account of code {r.status_code}. Try connection again?"
                if get_yn(msg):
                    return self.scrape(attempt)
                else:
                    return False
            except:
                # a non-HTTP error has occured, but can't think of what'd kick an error
                # Prolly certain types of returned data?
                print(
                    "We may have broken something...or someone may actually be a teapot...hang on..."
                )
                time.sleep(2)
                print("Trying again.")
                time.sleep(1)
                attempt += 1
                return self.scrape(attempt)
        else:
            # if we get here, chances are there was a bad request, but whatev
            print(
                f"I'm not sure what's going wrong, here, but we have had a SERIOUS series of errors."
            )


def enter():
    # just a stopper not tied to time.sleep
    return input("Press [enter] to continue...")


def get_time(timezone):
    # quick little function to apply same type of unix handling to our times as the ones
    # passed, just to help ensure our times are all jiving
    dt = datetime.now()
    unix = int(time.mktime(dt.timetuple()))
    utc = unix + timezone
    dte = datetime.utcfromtimestamp(utc).strftime("%A, %B %d")
    tme = datetime.utcfromtimestamp(utc).strftime("%I:%M %p")

    return dte, tme


def flatten(current, key="", result={}):
    # quick function to "flatten" the json to a singular k/v dictionary JSON style
    iter = 0
    if isinstance(current, dict):
        for k, v in current.items():
            if isinstance(v, list):
                for dic in v:
                    new_key = f"{k}.{iter}"
                    flatten(dic, new_key)
                    iter += 1
            else:
                new_key = f"{key}.{k}" if len(key) > 0 else k
                flatten(current[k], new_key, result)
    else:
        result[key] = current
    return result


def not_implemented():
    # place-holder for future expansion and reminder of gaps - All req's will be completed, none of the
    # base req's can have this holder
    print(
        "Sorry, that feature hasn't been built-out yet. Check back, and it may be.\nCheers!"
    )
    enter()


def werder(werds):
    # got tired of typing questions, so I tried to speed things up a bit using "reel werds"
    msg1 = "What is the "
    msg2 = "city's "
    msg3 = "name"
    msg4 = "zip code"
    msg5 = "state's "
    msg6 = "country's "
    msg7 = "two letter abbreviation"
    msg8 = "?\n> "
    msg9 = "ID# "

    if werds == "cin":
        cin = "".join([msg1, msg2, msg3, msg8])
        return cin
    elif werds == "ciz":
        ciz = "".join([msg1, msg2, msg4, msg8])
        return ciz
    elif werds == "sin":
        sin = "".join([msg1, msg5, msg7, msg8])
        return sin
    elif werds == "coin":
        coin = "".join([msg1, msg6, msg7, msg8])
        return coin
    elif werds == "cid":
        cid = "".join([msg1, msg2, msg9, msg8])
        return cid


def get_yn(prompt):
    # a simple function designed to handle a quick yes/no question
    err = "I couldn't catch that. Let's do this again."
    msg = input(f"{prompt} [y/n]\n> ")
    if not msg:
        return get_yn("You didn't type anything!")
    elif "y" in msg:
        if msg == "y" or msg == "yes" or msg == "ya":
            return True
        else:
            return get_yn(err)
    elif "n" in msg:
        if msg == "n" or msg == "no" or msg == "na":
            return False
        else:
            return get_yn(err)
    else:
        return get_yn(err)


# initialize and grab first pull of data from open weather
local = Locale()

# prebuilt dictionary of menu tree and commands
menu_dict = {
    "Main": {
        "Quick Weather": local.quick_weather,
        "View Current Locale": {
            "View Locale Information": local.display_location,
            "View Today's Detailed Forecast": local.display_weather,
            "View 5-day Forecast": not_implemented,
            "View Weather History": not_implemented,
            "Main Menu": "upone",
            "Exit Program": "exit",
        },
        "Find New Locale": {
            "Search By Name": local.name_search,
            "Search By City ID#": local.cid_search,
            "Search By Zip Code": local.zip_search,
            "Search By Geographic Coordinates": local.geo_search,
            "Main Menu": "upone",
            "Exit Program": "exit",
        },
        "Exit Program": "exit",
    }
}

# start up Menu class and pass prebuilt menu dictionary
menu = Menu("Main", menu_dict)

# technically the beginning of the program
print("\n\nHello, and welcome to the Wx-APY-thon 2500!\n")

# prepare program loop
menu.end_program = False
while not menu.end_program:
    menu.navigating = True
    while menu.navigating:
        menu.navigate()
    menu.end_program = True