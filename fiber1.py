def calc(x, y):
    return x * y


# Display a welcome message for the program.

print("\nWelcome to the fiber optic calculator 3000!\n")

# Get the company name from the user.

prompt1 = "What is the company's name for the order?\n"

# Get the number of feet of fiber optic to be installed from the user.

prompt2 = "How many feet are they looking to buy?\n"

# Set up variables

price = 0.87
company_name = ""
feet = ""

# Check the input company_name

bad_input = True
while bad_input:
    company_name = str(input(prompt1))
    if not company_name:
        print("\nYou didn't type anything.\n")
    else:
        bad_input = False

# Check the input feet

bad_input = True
while bad_input:
    try:
        feet = float(input(prompt2))
        bad_input = False
    except ValueError:
        print("\nYour input didn't seem right, try again.\n")

# Multiply the total cost as the number of feet times $0.87.

cost = calc(price, feet)

# Display the calculated information and company name.

print(
    f"\nThe company {company_name} wishes to buy {feet} feet of fiber optic cable. This will cost ${cost}.\n"
)
