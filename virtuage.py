# This week we will work with classes by creating a virtual garage. Your program will use the inheritance diagram from this week in order
# to create a parent class and two child classes.


# Your program will prompt the user to create at least one object of each type (Car and Pickup). Using a menu system and capturing user
# input your program will allow the user the choice of adding a car or pickup truck and define the vehicle's attributes. The program will
# use user input to define the vehicle's attributes.

# The options attributed in the parent class must be a python list containing a minimum of eight (8) options common to all vehicles. (i.e.
# power mirrors, power locks, remote start, backup camera, bluetooth, cruise control, etc).

# The user will choose from a list of options to add to the vehicle's options list and can must choose a minimum of one vehicle option per
# vehicle. When the user is finished adding vehicles to their virtual garage the program will output the vehicles in their garage and
# their attributes.

# The following information provides students with a breakdown of how this assignment will be assessed.

# 1. Object Oriented Programming and Inheritance - 30%
# Create a Vehicle class with the attributes and functions detailed in the class diagram. - 10%
# Create a Car class as a child of the Vehicle class with the attributes and functions detailed in the class diagram. - 10%
# Create a Pickup class as a child of the Vehicle class with the attributes and functions detailed in the class diagram. - 10%
# 2. Demonstrate usage of previously studied programming constructs (functions, conditionals, loops)  - 60%
# Using a function, display a menu prompting the user to add a Car or a Pickup to their virtual garage. - 15%
# Your program must allow the user to have multiple vehicles in their virtual garage and must have at least one Car and one Pickup. - 15 %
# Your program will prompt the user to define the attributes of the vehicles in their garage. - 10%
# The options attribute will be defined as a python list chosen by the user when presented with a menu of programmer chosen vehicle options
# that can apply to both cars and pickup trucks (i.e. power mirrors, power locks, remote start, backup camera, bluetooth, cruise control,
# etc) - 20%
# 3. When the user has finished adding and defining vehicles for their garage the program will output the vehicles with their accompanying
# attributes and options as specified by the user. -10 %


class Vehicle:
    def __init__(self, features):
        for key, value in features.items():
            if "Year" in key:
                self.year = value
            elif "Owner" in key:
                self.owname = value
            elif "Make" in key:
                self.make = value
            elif "Model" in key:
                self.model = value
            elif "Color" in key:
                self.color = value
            elif "Fuel Type" in key:
                self.ftype = value
            elif "Options" in key:
                self.options = value

    @classmethod
    def build_vehicle(cls, name, features):
        g_dict["Others"][name] = cls(features)

    def get_year(self):
        return self.year

    def get_make(self):
        return self.make

    def get_model(self):
        return self.model

    def get_color(self):
        return self.color

    def get_ftype(self):
        return self.ftype

    def get_options(self):
        return self.options


class Pickup(Vehicle):
    def __init__(self, features):
        for key, value in features.items():
            if "Cab Style" in key:
                self.cstyle = value
            elif "Bed Length" in key:
                self.blength = value
        super(Pickup, self).__init__(features)

    @classmethod
    def build_truck(cls, name, features):
        g_dict["Trucks"][name] = cls(features)

    def get_cstyle(self):
        return self.cstyle

    def get_blength(self):
        return self.blength


class Car(Vehicle):
    def __init__(self, features):
        for key, value in features.items():
            if "Engine Size" in key:
                self.esize = value
            elif "Doors" in key:
                self.doors = value
        super(Car, self).__init__(features)

    @classmethod
    def build_car(cls, name, features):
        g_dict["Cars"][name] = cls(features)
        return g_dict["Cars"][name]

    def get_esize(self):
        return self.esize

    def get_doors(self):
        return self.doors


class Menu:
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
        selection = input("Your selection?\n >")
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
                    print(itr)
                    if itr == sel:
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
        if check_open():
            msg = "The garage is still open, did you want to close it before exiting?"
            if get_yn(msg):
                self.navigating = False
                self.end_program = True
                print("Exiting")
                exit()
            else:
                return enter()
        else:
            self.navigating = False
            self.end_program = True
            print("Exiting")
            exit()


class G_Menu(Menu):
    def __init__(self, master_dictionary):
        self.opn = False
        self.saved = False
        self.master_data = master_dictionary
        self.vehicles = self.master_data.keys()
        self.num_vehicles = len(self.vehicles)
        self.parked_cars = []
        self.parked_trucks = []
        for key, value in self.master_data.items():
            for v in value.values():
                if v == "Car":
                    self.parked_cars.append(key)
                elif v == "Truck":
                    self.parked_trucks.append(key)

    def show_status(self):
        if self.opn:
            open_status = "open"
        else:
            open_status = "closed"
        if self.num_vehicles > 1 or self.num_vehicles == 0:
            plural = "s"
        else:
            plural = ""
        print(
            f"The garage has {str(self.num_vehicles)} vehicle{plural} stored and is currently {open_status}."
        )
        return enter()

    def open_garage(self):
        print("Garage is now open!")
        self.opn = True
        return enter()

    def close_garage(self):
        print("Garage is now closed!")
        self.opn = False
        return enter()

    def show_vehicles(self):
        if self.num_vehicles == 0 or self.num_vehicles > 1:
            if self.num_vehicles == 0:
                print("There are no vehicles in the Garage.")
                return enter()
            else:
                plural = "s"
        else:
            plural = ""

        print(f"There are currently {str(self.num_vehicles)} vehicles in our Garage.")
        print("Here are the vehicles, by their registered nicknames/VIN/Plate Numbers:")
        if len(self.parked_cars) > 1:
            print("There are no parked cars in the Garage.")
        else:
            print("-First, here are the cars:")
            for car in self.parked_cars:
                print(f"-->{car} - A {self.master_data[car]['MakeMod']}")
        if len(self.parked_trucks) == 0:
            print("There are no parked trucks in the Garage.")
        else:
            print("-And, here are the Trucks")
            for truck in self.parked_trucks:
                print(f"-->{truck} - A {self.master_data[truck]['MakeMod']}")
        print(
            f"This makes a total of {str(self.num_vehicles)} vehicle{plural} in the Garage."
        )
        return enter()

    def save(self):
        self.saved = True
        print("Save successful")
        enter()
        return self.master_data

    def update(self, dic):
        self.master_data = dic
        self.vehicles = self.master_data.keys()
        self.parked_cars = []
        self.parked_trucks = []
        for key, value in self.master_data.items():
            for v in value.values():
                if v == "Car":
                    self.parked_cars.append(key)
                elif v == "Truck":
                    self.parked_trucks.append(key)
        self.num_vehicles = len(self.vehicles)

    def inspect_vehicle(self, name=None, rem=False, srch=False):
        v_search = False
        o_search = False
        if self.num_vehicles < 1 and not rem and not srch:
            print("Sorry, there are no vehicles parked in the garage.")
            return enter()
        else:
            if srch or rem:
                if srch:
                    v_search = True
                    sch = name
                else:
                    pass
            else:
                msg = f"Would you like lookup a vehicle with the [owner]s name, or the [vehicle]s nickname?\n(type [owner] or [vehicle])\n> "
                inpt = input(msg)
                if "own" in inpt or "owner" in inpt or "veh" in inpt or "vehic" in inpt:
                    if "own" in inpt:
                        msg = "You wanted to lookup by owner, right?"
                        if get_yn(msg):
                            o_search = True
                            sch = None
                            while not sch or not isinstance(sch, str):
                                sch = input(f"Please type the owner's name:\n> ")
                            o_exists = omenu.inspect_owner(srch=True, name=sch)
                            if not o_exists:
                                msg = f"The name {sch} isn't registered with our Garage.  Would you like to do this now?"
                                if get_yn(msg):
                                    omenu.create_owner(name=sch)
                                else:
                                    print(
                                        "Sorry, can't look up a name that doesn't exist. Try again."
                                    )
                                    return enter()
                            else:
                                pass
                        else:
                            print("I'm sorry, I don't understand.")
                            return enter()
                    elif "veh" in inpt or "hic" in inpt:
                        msg = "You wanted to search by vehicle nickname, right?"
                        if get_yn(msg):
                            v_search = True
                            sch = input(f"Please type the vehicle's nickname:\n> ")
                        else:
                            print(
                                "I'm sorry, I can be sorta stupid. Let's start over, yea?"
                            )
                            return enter()
                    else:
                        msg = "I didn't quite get that, try again?"
                        if get_yn(msg):
                            return self.inspect_vehicle()
                        else:
                            return
        try:
            search = str(sch.lower())
            for vehicle in self.vehicles:
                if o_search:
                    v_owner = v_dict[vehicle]["Owner"].lower()
                    if v_owner in search or search in v_owner:
                        if search == v_owner:
                            msg = f"{v_owner.title()}'s vehicle {vehicle} found!  Was this the one you were looking for?"
                            if get_yn(msg):
                                msg = f"Would you like to see some quick details of {vehicle}?"
                                if get_yn(msg):
                                    self.display_vehicle(vehicle)
                                    return enter()
                elif v_search:
                    if search in vehicle.lower() or vehicle.lower() in search:
                        if vehicle.lower() == search:
                            if srch:
                                return True
                            else:
                                v_owner = v_dict[vehicle]["Owner"]
                                print(
                                    f'Vehicle "{vehicle.title()}" was found and is owned by {v_owner}.'
                                )
                                msg = "Is this the one you were looking for?"
                                if get_yn(msg):
                                    if not rem:
                                        msg = f"Would you like to see some quick details of {vehicle}?"
                                        if get_yn(msg):
                                            self.display_vehicle(vehicle)
                                            return enter()
                                        else:
                                            return enter()
                                    elif rem:
                                        if get_yn(
                                            f"Are you sure you want to delete {vehicle.title()}?"
                                        ):
                                            self.remove_vehicle(vehicle)
                                            return flush_delete(
                                                fvehicle=True,
                                                owner=v_owner,
                                                vehicle=vehicle,
                                            )
                                        else:
                                            return
                                else:
                                    msg = "Sorry, did you want to try looking up under a different parameter?"
                                    if get_yn(msg):
                                        return self.inspect_vehicle()
                                    else:
                                        print("I'm sorry we couldn't find it.")
                                        return enter()
                elif srch:
                    return False
        except ValueError:
            print("Couldn't find vehicle you're looking for.")
            enter()

    def display_vehicle(self, vehicle=None):
        if not vehicle:
            return self.inspect_vehicle()
        else:
            for key, value in self.master_data.items():
                if key.lower() == vehicle.lower():
                    print(f"Vehicle's Nickname = {key}")
                    for k, v in value.items():
                        print(f"{k}: {v}")

    def insert_vehicle(self, vehicle=None):
        if not self.opn:
            msg = f"Garage is closed right now, would you like to open it up?"
            if get_yn(msg):
                self.opn = True
                return self.insert_vehicle()
            else:
                return enter()
        else:
            if not vehicle:
                sch = input(f"What's the name of the vehicle?\n> ")
            else:
                sch = vehicle
            v_exists = vmenu.inspect_vehicle(sch, True, False)
            if v_exists:
                in_garage = self.inspect_vehicle(sch, False, True)
                if in_garage:
                    print(f'"{sch.title()}" is already in the garage!')
                    return enter()
                else:
                    sch = sch.title()
                    typ = v_dict[sch]["Type"]
                    owner = v_dict[sch]["Owner"]
                    yc = f"{v_dict[sch]['Year']} {v_dict[sch]['Color']}"
                    mm = f"{v_dict[sch]['Make']} {v_dict[sch]['Model']}"
                    g_dict[sch] = dict(
                        {"Type": typ, "Owner": owner, "YearCol": yc, "MakeMod": mm}
                    )
                    print(
                        f"Awesome!  That {mm.title()} named {sch.title()}, owned by {owner.title()} has entered the garage!"
                    )
                    enter()
                    return self.update(g_dict)

    def remove_vehicle(self, vehicle=None, owner=None, flush=False):
        if not self.opn and not flush:
            msg = f"Garage is closed right now, would you like to open it up?"
            if get_yn(msg):
                self.opn = True
                return self.remove_vehicle()
            else:
                return enter()
        else:
            if owner and not vehicle:
                owner_vehicles = []
                for key, value in g_dict.items():
                    for v in value.values():
                        if v == owner:
                            owner_vehicles.append(key)
                if len(owner_vehicles) >= 1:
                    for vehicle in owner_vehicles:
                        self.remove_vehicle(vehicle, owner, flush)
                    print(
                        f"Everything belonging to {owner} has been removed from the Garage."
                    )
                    return enter()
                elif len(owner_vehicles) == 0:
                    print("That registered owner didn't appear to own any vehicles")
                    return enter()
            if not vehicle:
                sch = input(f"What's the name of the vehicle?\n> ")
                v_exists = vmenu.inspect_vehicle(sch, True, False)
                if v_exists:
                    in_garage = self.inspect_vehicle(sch, False, True)
                    if not in_garage:
                        print(f'"{sch.title()}" isn\'t in the garage!')
                        return enter()
                    else:
                        sch = sch.title()
                        owner = v_dict[sch]["Owner"]
                        mm = f"{v_dict[sch]['Make']} {v_dict[sch]['Model']}"
                        dictionary = {
                            key: value
                            for key, value in self.master_data.items()
                            if key != sch
                        }
                        print(
                            f"Awesome!  That {mm.title()} named {sch.title()}, owned by {owner.title()} has left the garage!"
                        )
                        enter()
                        return self.update(dictionary)
            elif vehicle:
                dictionary = {
                    key: value
                    for key, value in self.master_data.items()
                    if key is not vehicle
                }
                self.update(dictionary)


class O_Menu(Menu):
    def __init__(self, o_dict):
        self.main_dict = o_dict
        self.owners = o_dict.keys()

    def show_owners(self):
        if len(self.owners) < 1:
            print("There are currently no registered owners.")
            enter()
            return
        print("The following registered owners have been found:")
        for owner in self.owners:
            print(f" - {owner.title()}")
        enter()

    def inspect_owner(self, rem=False, srch=False, name=None):
        if not srch:
            sch = input(f"Please type the owner you'd like to search.\n> ")
        else:
            sch = name
        try:
            search = str(sch.lower())
            for owner in self.owners:
                if owner.lower() == search.lower():
                    if srch:
                        return True
                    else:
                        print(f"Owner {owner.title()} was found. ")
                        if not rem:
                            num_vehicles = len(self.main_dict[owner]["Vehicles"])
                            print(
                                f"Owner {owner.title()} has {num_vehicles} registered vehicles."
                            )
                            enter()
                            return
                        elif rem:
                            if get_yn(
                                f"Are you sure you want to delete {owner.title()}?"
                            ):
                                return self.delete_owner(owner)
                            else:
                                return
                elif srch:
                    return False
        except ValueError:
            print("Couldn't find who you're looking for.")
            enter()

    def create_owner(self, name=None):
        if not name:
            ownr = input("What name would you like to register?\n> ")
        else:
            ownr = name
        if not ownr:
            print("You didn't type anything! Try again.")
            return self.create_owner()
        elif self.inspect_owner(name=ownr, srch=True):
            print(
                f"There is already a registered owner by the name of {ownr.title()}! Try again."
            )
            return self.create_owner()
        else:
            self.main_dict[ownr.title()] = dict({"Vehicles": {}})
            self.owners = self.main_dict.keys()
            print(f"Owner {ownr.title()} has been successfully registered!")
            enter()

    def delete_owner(self, owner=None):
        if not owner:
            return self.inspect_owner(rem=True)
        else:
            msg = f"Are you sure you want to delete {owner} and all of their registered vehicles?"
            if get_yn(msg):
                self.main_dict = {
                    key: value
                    for key, value in self.main_dict.items()
                    if key is not owner
                }
                self.owners = self.main_dict.keys()
                return flush_delete(True, False, False, owner)
            else:
                print("Ok, not deleting...")
                return enter()

    def remove_owner_vehicle(self, owner, vehicle):
        self.main_dict[owner]["Vehicles"] = {
            key: value
            for key, value in self.main_dict[owner]["Vehicles"].items()
            if key is not vehicle
        }

    def save(self):
        return self.main_dict

    def update(self, o_dict):
        self.main_dict = o_dict
        self.owners = self.main_dict.keys()


class V_Menu(Menu):
    reqs_list = [
        "Type",
        "Owner",
        "Year",
        "Make",
        "Model",
        "Color",
        "Fuel Type",
        "Options",
    ]
    options = [
        "power mirrors",
        "power locks",
        "power steering",
        "power windows",
        "remote start",
        "backup camera",
        "bluetooth",
        "cruise control",
        "mp3 entertainment center",
    ]

    def __init__(self, dictionary):
        self.data = dictionary
        self.vehicles = dictionary.keys()

    def show_vehicles(self):
        if len(self.vehicles) < 1:
            print("There are currently no registered vehicles.")
            enter()
            return
        print("The following registered vehicles have been found:")
        for vehicle in self.vehicles:
            print(
                f" - Vehicle: \"{vehicle.title()}\" - Type: \"{self.data[vehicle]['Type']}\""
            )
        enter()

    def create_vehicle(self):
        inpt = input(
            f"What is the nickname/VIN/Plate Number you'd like to register?\n> "
        )
        if not inpt:
            print("You didn't type anything!")
            return self.create_vehicle()
        elif self.inspect_vehicle(name=inpt, srch=True):
            msg = "There's already a vehicle registered as that! Try something else?"
            if get_yn(msg):
                return self.create_vehicle()
            else:
                return enter()
        else:
            name = inpt.title()
            temp_dict = {name: {}}
            print(f"What type of vehicle is {name}?")
            inpt = input("[1] Car\n[2] Truck\n[3] Other\n> ")
            try:
                sel = int(inpt)
                if sel == 1:
                    reqs = self.reqs_list
                    reqs.append("Engine Size")
                    reqs.append("Doors")
                elif sel == 2:
                    reqs = self.reqs_list
                    reqs.append("Cab Style")
                    reqs.append("Bed Length")
                else:
                    print(
                        "We aren't accepting none car/truck registrations atm, sorry."
                    )
                    return
                print("Let's run through the build of this vehicle, shall we?")
                for subject in reqs:
                    if subject == "Options":
                        print("Just type y/n to the following options...")
                        temp_list = []
                        for option in self.options:
                            msg = f"Vehicle Options: {option}"
                            if get_yn(msg):
                                temp_list.append(option)
                            else:
                                pass
                        temp_dict[name][subject] = temp_list
                    elif subject == "Type":
                        pass
                    elif subject == "Owner":
                        sub = input(f"The vehicle's {subject}?\n> ")
                        sub = sub.title()
                        o_exists = omenu.inspect_owner(srch=True, name=sub)
                        if o_exists:
                            msg = f"The owner {sub} is already registered with the Garage.  Append this vehicle to them?"
                            if get_yn(msg):
                                temp_dict[name][subject] = sub
                            else:
                                return
                        else:
                            msg = f"The owner {sub} is not registered with the Garage.  Would you like to do this now?"
                            if get_yn(msg):
                                temp_dict[name][subject] = sub
                                omenu.create_owner(name=sub)
                            else:
                                pass
                    else:
                        sub = input(f"The vehicle's {subject}?\n> ")
                        temp_dict[name][subject] = sub
                print(
                    "Let's pause for a second, and make sure we have everything right."
                )
                enter()
                for key, value in temp_dict[name].items():
                    msg = f"--> For {key}, I've got {value}"
                    print(msg)
                msg = "Is that all correct?"
                if get_yn(msg):
                    print("Awesome!  Saving all this now.")
                    v_dict[name] = temp_dict[name]
                    yearcol = (v_dict[name]["Year"]) + " " + (v_dict[name]["Color"])
                    makemod = (v_dict[name]["Make"]) + " " + (v_dict[name]["Model"])
                    if sel == 1:
                        owname = v_dict[name]["Owner"]
                        v_dict[name]["Type"] = "Car"
                        v_dict[name]["Object"] = Car(v_dict[name])
                        o_dict[owname]["Vehicles"][name] = dict(
                            {"Type": "Car", "YearCol": yearcol, "MakeMod": makemod}
                        )
                    elif sel == 2:
                        owname = v_dict[name]["Owner"]
                        v_dict[name]["Type"] = "Truck"
                        v_dict[name]["Object"] = Pickup(v_dict[name])
                        o_dict[owname]["Vehicles"][name] = dict(
                            {"Type": "Truck", "YearCol": yearcol, "MakeMod": makemod}
                        )
                    print("Success, fleshbag!")
                    return enter()
                else:
                    print("**Deep, Robotic Sigh**...ok")
                    msg = "Would you like to start over?"
                    if get_yn(msg):
                        return self.create_vehicle()
                    else:
                        return enter()

            except TypeError:
                print("Sorry, we didn't understand what you meant to do.  Try again.")
                return self.create_vehicle()

    def inspect_vehicle(self, name=None, srch=False, rem=False):
        o_search = False
        v_search = False
        if srch:
            v_search = True
            sch = name
        elif not srch:
            o_search = False
            v_search = False
            msg = f"Would you like lookup a vehicle with the [owner]s name, or the [vehicle]s nickname?\n(type [owner] or [vehicle])\n> "
            inpt = input(msg)
            if "own" in inpt or "veh" in inpt:
                if "own" in inpt:
                    msg = "You wanted to lookup by owner, right?"
                    if get_yn(msg):
                        o_search = True
                        sch = None
                        while not sch or not isinstance(sch, str):
                            sch = input(f"Please type the owner's name:\n> ")
                        o_exists = omenu.inspect_owner(srch=True, name=sch)
                        if not o_exists:
                            msg = f"The name {sch} isn't registered with our Garage.  Would you like to do this now?"
                            if get_yn(msg):
                                omenu.create_owner(name=sch)
                            else:
                                print(
                                    "Sorry, can't look up a name that doesn't exist. Try again."
                                )
                                enter()
                                return self.inspect_vehicle()
                        else:
                            pass
                    else:
                        print("I'm sorry, I don't understand.")
                        enter()
                        return self.inspect_vehicle()
                elif "veh" in inpt:
                    msg = "You wanted to search by vehicle nickname, right?"
                    if get_yn(msg):
                        v_search = True
                        sch = input(f"Please type the vehicle's nickname:\n> ")
                    else:
                        print(
                            "I'm sorry, I can be sorta stupid. Let's start over, yea?"
                        )
                        return self.inspect_vehicle()
        else:
            sch = name
        try:
            search = str(sch.lower())
            for vehicle in self.vehicles:
                if o_search:
                    v_owner = v_dict[vehicle]["Owner"].lower()
                    if v_owner in search or search in v_owner:
                        if search == v_owner:
                            msg = f"{v_owner.title()}'s vehicle {vehicle} found!  Was this the one you were looking for?"
                            if get_yn(msg):
                                msg = f"Would you like to see the full details of {vehicle}?"
                                if get_yn(msg):
                                    self.display_vehicle(vehicle)
                                    return enter()
                                else:
                                    return
                            else:
                                pass

                elif v_search:
                    if vehicle.lower() == search:
                        if srch:
                            return True
                        elif rem:
                            if get_yn(
                                f"Are you sure you want to delete {vehicle.title()}?"
                            ):
                                return self.delete_vehicle(vehicle)
                            else:
                                return
                        else:
                            msg = f"Vehicle {vehicle.title()} was found.  Was this the one you were looking for?"
                            if get_yn(msg):
                                msg = f"Would you like to see the full details of {vehicle}??"
                                if get_yn(msg):
                                    self.display_vehicle(vehicle)
                                    return enter()
                                else:
                                    return
                            else:
                                pass

                elif srch:
                    return False
        except:
            print("Couldn't find vehicle you're looking for, sorry.")
            enter()

    def display_vehicle(self, vehicle=None):
        if not vehicle:
            return self.inspect_vehicle()
        else:
            for key, value in self.data.items():
                if key.lower() == vehicle.lower():
                    print(f"Vehicle's Nickname = {key}")
                    for k, v in value.items():
                        print(f"{k}: {v}")

    def delete_vehicle(self, vehicle=None, owner=None, fflush=False):
        if owner and not vehicle:
            owner_vehicles = []
            owname = owner
            for key, value in g_dict.items():
                for v in value.values():
                    if v == owner:
                        owner_vehicles.append(key)
            if len(owner_vehicles) >= 1:
                for ve in owner_vehicles:
                    self.delete_vehicle(vehicle=ve, fflush=fflush)
                print(f"All of {owname}'s vehicles have been deleted from registry.")
            elif len(owner_vehicles) == 0:
                print("That registered owner didn't appear to own any vehicles")
                return enter()
        elif not vehicle:
            return self.inspect_vehicle(rem=True)

        self.data = {
            key: value for key, value in self.data.items() if key is not vehicle
        }
        self.vehicles = self.data.keys()
        if fflush:
            pass
        else:
            return flush_delete(False, True, False, None, vehicle)

    def show_options(self):
        print("These are the options currently configured.")
        for option in self.options:
            print(f"--{option}--")

    def create_option(self):
        inpt = "What's the name if this new option?"
        if not inpt:
            print("You didn't type anything")
        else:
            try:
                option = str(inpt)
                msg = f"So, you wanted to add {option}, correct?"
                if get_yn(msg):
                    self.options.append(option)
                else:
                    return
            except ValueError:
                print("I'm sorry, we didn't understand")
                return self.create_option

    def delete_option(self):
        inpt = "What's the name of the option you'd like to delete?"
        if not inpt:
            print("You didn't type anything")
            return self.delete_option()
        elif inpt.lower() in self.options.lower():
            msg = f"Option {inpt} found.  Sure you want to delete it?"
            if get_yn(msg):
                self.options.pop(inpt)
            else:
                return
        else:
            print("We didn't find the option you were looking for.")
            return self.delete_option()

    def save(self):
        return self.data

    def update(self, dictionary):
        self.data = dictionary
        self.vehicles = dictionary.keys()


def get_yn(prompt):
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


def enter():
    return input("Press [enter] to continue...")


def check_open():
    return virtuage.opn


def flush_delete(
    fowner=False,
    fvehicle=False,
    fgarage=False,
    owner=None,
    vehicle=None,
):

    if fowner:
        vmenu.delete_vehicle(owner=owner, fflush=True)
        virtuage.remove_vehicle(owner=owner, flush=True)
        save_update()
    elif fvehicle:
        virtuage.remove_vehicle(owner=owner)
        omenu.remove_owner_vehicle(owner, vehicle)
    elif fgarage:
        virtuage.remove_vehicle(vehicle)
        omenu.remove_owner_vehicle(owner, vehicle)
        save_update()


def save_update():
    o_dict = omenu.save()
    omenu.update(o_dict)
    v_dict = vmenu.save()
    vmenu.update(v_dict)
    g_dict = virtuage.save()
    virtuage.update(g_dict)


g_dict = {
    "Test Vehicle": {
        "Type": "Car",
        "Owner": "John Smith",
        "YearCol": "2019 Red",
        "MakeMod": "Chevy Impala",
    }
}

v_dict = {
    "Test Vehicle": {
        "Type": "Car",
        "Owner": "John Smith",
        "Esize": "350",
        "Doors": "4d",
        "Year": "2019",
        "Make": "Chevy",
        "Model": "Impala",
        "Color": "Red",
        "Ftype": "Gasoline",
        "Options": ["Power Mirrors", "Power Locks"],
    }
}

o_dict = {
    "John Smith": {
        "Vehicles": {
            "Test Vehicle": {
                "Type": "Car",
                "YearCol": "2019 Red",
                "MakeMod": "Chevy Impala",
            }
        }
    }
}

virtuage = G_Menu(g_dict)
vmenu = V_Menu(v_dict)
omenu = O_Menu(o_dict)

menu_dict = {
    "Main": {
        "Garage": {
            "Manage Garage": {
                "Garage Status": virtuage.show_status,
                "Open Garage": virtuage.open_garage,
                "Close Garage": virtuage.close_garage,
                "Save Garage": virtuage.save,
                "Return to Garage Menu": "upone",
                "Exit Program": virtuage.exit_program,
            },
            "Manage Parked Vehicles": {
                "Show Vehicles": virtuage.show_vehicles,
                "Inspect a Vehicle": virtuage.inspect_vehicle,
                "Insert a Vehicle": virtuage.insert_vehicle,
                "Remove Vehicle": virtuage.remove_vehicle,
                "Return to Garage Menu": "upone",
                "Exit Program": virtuage.exit_program,
            },
            "Return to Main Menu": "upone",
            "Exit Program": "exit",
        },
        "Vehicles": {
            "Manage Vehicles": {
                "Show Vehicles": vmenu.show_vehicles,
                "Create a Vehicle": vmenu.create_vehicle,
                "Inspect a Vehicle": vmenu.inspect_vehicle,
                "Delete a Vehicle": vmenu.delete_vehicle,
                "Return to Vehicle Menu": "upone",
                "Exit Program": vmenu.exit_program,
            },
            "Manage Vehicle Options": {
                "View options": vmenu.show_options,
                "Create an option": vmenu.create_option,
                "Remove an option": vmenu.delete_option,
                "Return to Vehicle Menu": "upone",
                "Exit Program": vmenu.exit_program,
            },
            "Return to Main Menu": "upone",
            "Exit Program": "exit",
        },
        "Owners": {
            "Show Registered Owners": omenu.show_owners,
            "Inspect an Owner": omenu.inspect_owner,
            "Create an Owner": omenu.create_owner,
            "Delete an Owner": omenu.delete_owner,
            "Return to Vehicle Menu": "upone",
            "Exit Program": omenu.exit_program,
        },
        "Exit Program": "exit",
    }
}

menu = Menu("Main", menu_dict)

print("Hello, and welcome to Virtuage 3, a virtual vehicular garage thingy!")

menu.end_program = False
while not menu.end_program:

    menu.navigating = True
    while menu.navigating:
        menu.navigate()

    end_program = True