# This week we will create a program that performs file processing activities. Your program this week will use the OS library in
# order to validate that a directory exists before creating a file in that directory. Your program will prompt the user for the
# directory they would like to save the file in as well as the name of the file. The program should then prompt the user for their
# name, address, and phone number. Your program will write this data to a comma separated line in a file and store the file in the
# directory specified by the user.

# Once the data has been written your program should read the file you just wrote to the file system and display the file contents
# to the user for validation purposes.

# Submit a link to your Github repository.

import os
import csv
import time


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


def csv_handler(path, typ="default"):
    if typ == "default":
        with open(path, "w") as f:
            writer = csv.writer(f, delimiter=",")
            info = get_info()
            writer.writerow(info)
    elif typ == "append":
        with open(path, "a") as f:
            writer = csv.writer(f, delimiter=",")
            info = get_info()
            writer.writerow(info)
    print("Let's verify the writing, yea?")
    time.sleep(2)
    with open(path, "r") as f:
        reader = csv.reader(f, delimiter=",")
        line_count = 0
        empty_count = 0
        for row in reader:
            if row:
                print(f"---->{row[0]} \t {row[1]} \t {row[2]}.")
                line_count += 1
            else:
                line_count += 1
                empty_count += 1
                pass
    print(f"Processed {line_count} lines, {empty_count} of which were empty.")
    time.sleep(1)
    return user_handler()


def get_info():
    uinfo = []
    uname = ""
    uadd = {}
    addp = ["House Number", "Street Name", "City Name", "State Name", "Zip Code"]
    uphn = ""

    while not uname:
        uname = input("Please type your:\nName?\n> ").lower().title()
    while not uadd:
        for item in addp:
            uadd[item] = input(f"{item}?\n> ")
    while not uphn:
        uphn = input("Phone number?\n> ")
    addr = f'{uadd["House Number"]} {uadd["Street Name"]} {uadd["City Name"]} {uadd["State Name"]} {uadd["Zip Code"]}'
    uinfo = [uname, uphn, addr]
    return uinfo


def user_handler():
    uidir = ""
    while not uidir:
        uidir = input("Please type the directory you wish to use.\n> ")
    # validate with them
    msg = f"You wanted to use {uidir}, correct?"
    if get_yn(msg):
        # check if directory exists
        dir_exists = os.path.isdir(uidir)
        if dir_exists:
            # prompt if still want use
            msg = f"The directory {uidir} exists. Would you like to utilize it?"
            if get_yn(msg):
                # use
                uifil = ""
                while not uifil:
                    uifil = input(
                        "Please type the name of the file you'd like to save.\n> "
                    )
                msg = f"You wanted to use {uifil}, correct?"
                if get_yn(msg):
                    # check if dir ends with slash
                    if str.endswith(uifil, "/"):
                        path = uidir + uifil
                    else:
                        path = uidir + "/" + uifil
                    fil_exists = os.path.isfile(path=path)
                    if fil_exists:
                        msg = f"File {uifil} already exists, overwrite?"
                        if get_yn(msg):
                            # overwrite
                            return csv_handler(path=path)
                        elif get_yn("Append?"):
                            # append
                            return csv_handler(path=path, typ="append")
                        else:
                            return NotImplemented
                    else:
                        msg = f"File {uifil} doesn't exist. Create now?"
                        if get_yn(msg):
                            # create and write
                            return csv_handler(path)
                        else:
                            # quit I guess
                            pass
                else:
                    return user_handler()
            else:
                # prompt for a different dir
                return user_handler()
        else:
            # prompt if you'd like to make it
            msg = f"The directory {uidir} doesn't exist. Would you like to make it now?"
            if get_yn(msg):
                os.makedirs(uidir)
                uifil = ""
                while not uifil:
                    uifil = input(
                        "Please type the name of the file you'd like to save.\n> "
                    )
                msg = f"You wanted to use {uifil}, correct?"
                if str.endswith(uidir, "/"):
                    path = uidir + uifil
                else:
                    path = uidir + "/" + uifil
                if get_yn(msg):
                    return csv_handler(path)
                else:
                    return user_handler()
            else:
                return user_handler()
    else:
        return user_handler()


end_program = False
while not end_program:
    user_handler()
    end_program = True