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
        self.navigating = True
        self.build_menu()
        selection = input("Your selection?\n> ")
        return self.select(selection)

    def select(self, selection):
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

    def __init__(self, json={}):
        pass

    def update(self, json={}):
        pass

    def scrape(self):
        # this will be the primary API actor
        parameters = {
            "id": self.city_id,
            "appid": API,
            "units": "imperial",
            "lang": "en",
        }
        url = "https://api.openweathermap.org/data/2.5/weather"

        try:
            r = requests.get(url, parameters)
            while r.status_code == requests.codes.ok:  # pylint: disable=no-member
                data = json.loads(r.text)
                break
        except:
            print("We may have broken something...Hang on.")
        return data


def enter():
    # just a stopper not tied to time.sleep
    return input("Press [enter] to continue...")


def flatten(current, key="", result={}):
    # quick function to "flatten" the json to a singular k/v dictionary
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


def get_yn(prompt):
    # a simple function designed to handle a quick yes/no question
    err = "I couldn't catch that. Let's do this again."
    msg = input(f"{prompt} [y/n]\n> ")
    if not msg:
        return get_yn(err)
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


locale = Locale()
menu_dict = {
    "Main": {
        "View Current Locale": {
            "View Current Weather": locale.scrape,
            "View 5-day Forecast": NotImplemented,
            "View Weather History": NotImplemented,
            "Main Menu": "upone",
            "Exit Program": "exit",
        },
        "Find New Locale": {
            "Search By Name": NotImplemented,
            "Search By Zip Code": NotImplemented,
            "Main Menu": "upone",
            "Exit Program": "exit",
        },
        "Exit Program": "exit",
    }
}

menu = Menu("Main", menu_dict)

# technically the beginning of the program
print("Hello, and welcome to the Wx-APY-thon 2500!\n")

# prepare program loop
menu.end_program = False
while not menu.end_program:
    menu.navigating = True
    while menu.navigating:
        menu.navigate()
    menu.end_program = True