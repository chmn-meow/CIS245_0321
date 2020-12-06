# we are going to utilize the package numpy for its natural log function
import numpy as np


# we're going to use a dictionary lookup, to speed selection


def lookup(letter):
    ltr_dic = {"d": "days", "m": "months", "q": "quarters", "y": "years"}
    letters = ltr_dic.keys()
    if letter in letters:
        return ltr_dic[letter]
    else:
        return False


def simple_int(money, interest):
    # A = (P*r*t) + P
    ret = (money * (interest / 100)) + money
    return ret


# The formula to calculate the doubling time of an investment is as follows:
# T= (ln(2))/(ln(1 + r/100)) ~= 72/r
# T = time required.
# ln is just a natural log.
# r = rate per compounding period.
# ~= is used as a rate counter-balance estimate
# because it's useful to calculate based on a 72 estimate as well to help account for rate fluctuation
# also, it's easier to do in your head, and useful as a sanity check
# 72 is based on the investment tool called the "rule of 72"
# this calculation is a constant, so actual dollar amounts do not matter
# as investment amount does not matter, it's merely aesthetic.
# we will be calculating rule 72, compound interest, and simple interest

# initialize and get variables

cp = "Compounding Periods"

# we're going to use three separate while structures to cleanly capture for unique errors

# input and validation on the investment prompt

bad_input = True
while bad_input:
    investment = input("\nHow much are you looking to invest?\n")

    try:
        inv = float(investment)
        bad_input = False
    except ValueError:
        print("\nPlease try that again.\n")
    except TypeError:
        print("\nAre you sure that was a number?\n")


# input and validation on the interest prompt

bad_input = True
while bad_input:
    rate = input(
        "\nWhat compounding rate are you wanting to calculate? (please input full pecentage without symbols)\n"
    )

    try:
        r = float(rate)
        if r <= 0:
            print("\nThat is an invalid number for the purposes of this calculation!\n")
            raise ValueError
        else:
            pass
        bad_input = False
    except TypeError:
        print("\nYour input needs to be a positive percentage value, please.\n")
    except ValueError:
        print("\nYour input needs to be a positive percentage value, please.\n")

# input and validation on compounding periods

bad_input = True
while bad_input:
    inpt = input(
        "\nPlease input the type of compounding periods.\n Type 'd' for 'day', 'm' for 'month', 'q' for 'quarters' and 'y' for 'year'.\n Just hit enter if unknown:\n"
    )
    if not inpt:
        bad_input = False
    else:
        try:
            period = str(inpt.lower())
            if len(period) == 1:
                cp = lookup(period)
                if cp == False:
                    raise ValueError
                else:
                    bad_input = False
            else:
                raise ValueError
        except ValueError:
            print("\nPlease do not put in numbered values, or values not on list.\n")

# calculation

mtt = (np.log(2)) / (np.log(1 + r / 100))
emtt = 72 / r

# A = (P*r*t) + P


sim = inv
dub_sim = sim * 2

prin = inv
rt = r
t = 0

while sim <= dub_sim:
    sim = simple_int(sim, rt)
    t += 1
    if sim >= dub_sim:
        break


print(
    f"\nYour mean time to (mtt) double your initial investment of ${inv}, based on a compounding interest rate of {r}%, is {mtt} {cp}, and your 'rule 72' estimated mtt is {emtt} {cp}.  However, it's calculated to take {t} {cp} at a simple, non-compounding, rate of {r}%. Have a nice day!\n"
)