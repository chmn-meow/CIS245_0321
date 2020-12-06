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
CITY = str(os.environ.get("CITYID"))


def flatten(current, key="", result={}):
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


def scrape_data(
    appid=API,
    mode="",
    units="imperial",
    lang="en",
    cityid=CITY,
):

    parameters = {"id": cityid, "appid": appid, "units": units, "lang": lang}
    try:
        json_request = requests.get(
            "https://api.openweathermap.org/data/2.5/weather", parameters
        )
        raw = json.loads(json_request.text)
        reorg = flatten(raw)

    except:
        print("Something happened...")

    return reorg, raw


def fetch(
    typ="",
    prompt="\nType something\n",
    err_msg="\nYour input didn't seem right, please try again.\n",
    err=False,
):
    # prepare for while loop
    bad_input = True

    # check real quick if fetch called itself
    if err:
        print(err_msg)

    # while loop makes sure we have something we want before moving on
    while bad_input:

        # we us try here to catch our errors
        try:
            # this is to handle all numbers
            if typ == "float":
                err_msg = "\nAre you sure you put in a number?\n"
                inpt = float(input(prompt))
                bad_input = False

            # this is to handle single or double character answers for measurment abbreviations
            elif typ == "chrs":
                s_chrs = ["c", "n", "i", "d", "z", "p", "e", "x", "t"]
                d_chrs = ["cn", "id", "ex"]
                keywords = ["city", "name", "id", "zip", "code", "exit"]

                inpt = (input(prompt)).lower()
                if not inpt:
                    err_msg = "\nYou didn't type anything!\n"
                    raise ValueError
                elif len(inpt) == 1 and s_chrs in inpt:
                    if inpt == "c" or inpt == "n":
                        return "city_name"
                    elif inpt == "i":
                        return "city_id"
                    elif inpt == "z":
                        return "zip_code"
                    elif inpt == "x":
                        return "exit_code"
                    else:
                        err_msg = "\nI'm not quite sure what you meant by that. Please try again.\n"
                        raise ValueError
                    bad_input = False

                elif len(inpt) == 2 and d_chrs in inpt:
                    if inpt == "cn":
                        return "city_name"
                    elif inpt == "id":
                        return "city_id"
                    elif inpt == "ex":
                        return "exit_code"
                    else:
                        err_msg = f"\nDid you mean to type '{inpt}'?\n'"
                        raise ValueError
                elif len(inpt) >= 3 and keywords in inpt:
                    if inpt == "":
                        pass
                    err_msg = "\nAre you sure you hit the right characters?\n"
                    raise ValueError
                else:
                    bad_input = False

            # this is to handle a simple yes/no question
            elif typ == "yn":
                inpt = input(prompt)
                if not inpt:
                    err_msg = "\nYou didn't type anything!\n"
                    raise ValueError
                elif len(inpt) > 1:
                    err_msg = "\nPlease only type 'y' or 'n'.\n"
                    raise ValueError
                elif "y" not in inpt and "n" not in inpt:
                    err_msg = "\nDid you hit the wrong key?\n"
                    raise ValueError
                else:
                    bad_input = False

            # this is to handle any other kinds of default input
            else:
                inpt = input(prompt)
                bad_input = False

        # catch the error(s) and call self
        except ValueError:
            err = True
            return fetch(typ, prompt, err_msg, err)

    # pass inpt back to caller
    return inpt


# quick test/debug items
# processed, raw_json = scrape_data()
# print(f"\n\n{processed}")
# print(f"\n\n{raw_json}")
# print(flatten(raw))

# technically the beginning of the program
print("Hello, and welcome to the WeatherAPython 2000!\n")

# prepare actual meat of the program.
end_program = False
while not end_program:

    ser_prompt = f"\nHow would you like to look up your weather?\nType 'c/n/cn/city/name/city name' for city name\nType 'i/id' for city id\nType 'z/zip' for zip code\ntype 'x/ex/exit' to quit.\nLookup: "

    end_program = True