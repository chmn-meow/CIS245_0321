# this week's req's
# This week we will work with functions. For this week’s assignment, write a program that uses a function to convert miles to kilometers.
# Your program should prompt the user for the number of miles driven then call a function which converts miles to kilometers.
# The program should then display the total miles and the kilometers.

# We will be using a simple formula for converting
# but, we'll go both ways for future utility
# mi -> km is mi * 1.609344
# km -> mi is km / 1.609344
# for now, we're just going to go with a global constant
CONST = 1.609344

# define dict for future util
units_of_measure = {
    "metric": {"distance": [], "mass": [], "volume": []},
    "imperial": {"distance": [], "mass": [], "volume": []},
}

# define the function. Try to leave simple and open for future utility; decide later for dict lookup inside/outside of function call
def unit_conversion(st_unit, amount, st_type=0):
    if st_unit == "mi":
        # if we're converting mi -> km
        conv = amount * CONST
        conv_msg = f"\n{amount} miles converts to {conv} kilometers.\n"
    elif st_unit == "km":
        # if we're converting km -> mi
        conv = amount / CONST
        conv_msg = f"\n{amount} kilometers converts to {conv} miles.\n"
    else:
        # we've experienced some sort of unk error
        conv_msg = "\nUoM error. We didn't use the right calculation.\n"

    return conv_msg


# define fetch function to allow for quick expansion of utility
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
            elif typ == "chr":
                inpt = (input(prompt)).lower()
                if not inpt:
                    err_msg = "\nYou didn't type anything!\n"
                    raise ValueError
                elif len(inpt) == 1:
                    if "k" not in inpt and "m" not in inpt:
                        err_msg = "\nAre you sure you hit the right character?\n"
                        raise ValueError
                    else:
                        if inpt == "k":
                            inpt = "km"
                        elif inpt == "m":
                            inpt = "mi"
                        bad_input = False
                elif len(inpt) > 2:
                    err_msg = "\nPlease type the two characters only.\n"
                    raise ValueError
                elif "km" not in inpt and "mi" not in inpt:
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


# technically, the beginning of the program
print("\nHello, and welcome to the ConVnit 3000!\n")

# true program start
end_program = False
while not end_program:

    # we need to know what uom they are trying to convert
    uom_prompt = "\nWhat unit of measure shall we start with?\nType 'k/km' for kilometers, 'm/mi' for miles: "
    uom = fetch("chr", uom_prompt)

    # now we just need to grab how many units we're converting
    amount_prompt = f"\nEnter the number of {uom}: "
    amount = fetch("float", amount_prompt)

    # just print real quick the calc results
    print(unit_conversion(uom, amount))

    # ask for continue.  If yes, continue loop.  If no, terminate.
    cont_prompt = "Would you like to do another calculation?\n(y/n): "
    ans = fetch("yn", cont_prompt)
    if ans == "y":
        pass
    elif ans == "n":
        print(
            "\nThanks for utilizing the ConVnit 3000.\nBlessings of Cthulhu upon you!"
        )
        end_program = True