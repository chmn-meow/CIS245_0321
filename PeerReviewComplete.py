# Reviewer: Jayson Davidson
# Review Date: 11-Dec-20
# Below is a simple program with 10 issues (some are syntax errors and some are logic errors.  You need to identify the issues and correct them.

import random
import time


def displayIntro():
    print(
        """You are in a land full of dragons. In front of you,
	you see two caves. In one cave, the dragon is friendly
	and will share his treasure with you. The other dragon
	is greedy and hungry, and will eat you on sight."""
    )
    print()


def chooseCave():
    cave = ""

    # while cave != '1' and cave != '2':
    #   print('Which cave will you go into? (1 or 2)')
    #   cave = input()
    #   return caves
    while cave != "1" and cave != "2":
        print("which cave will you go into? (1 or 2)")
        cave = input()
        return cave
    # inconsistent usage of tabs vs spaces.  Choose one, keep one.  Also,
    # You erroneously returned 'caves' instead of 'cave'


def checkCave(chosenCave):
    print("You approach the cave...")
    # sleep for 2 seconds
    time.sleep(2)
    print("It is dark and spooky...")
    # sleep for 2 seconds

    # time.sleep(3)
    time.sleep(2)
    # did this for consistency.  Also, your comments said '2', rather than '3'

    print("A large dragon jumps out in front of you! He opens his jaws and...")
    print()
    # sleep for 2 seconds
    time.sleep(2)
    friendlyCave = random.randint(1, 2)

    if chosenCave == str(friendlyCave):
        print("Gives you his treasure!")
    else:

        # print 'Gobbles you down in one bite!'
        print("Gobbles you down in one bite!")
        # you were using python 2 syntax, python 3 requires the
        # statement be joined and parenthesized
        # Also, this whole function is tabbed vs spaced, not an issue here,
        # but if you were to add code, just make sure to be consistent
        # pick one and stick to it, it'll help reduce errors


playAgain = "yes"
# while playAgain = 'yes' or playAgain = 'y':
while playAgain == "yes" or playAgain == "y":
    # '=' means 'equals' as in 'is/assigned'
    # '==' means 'equals' as in comparatively (assignor vs. comparator)

    displayIntro()

    # caveNumber = choosecave()
    caveNumber = chooseCave()
    # if you have issues with camel-casing, try using underscores instead
    # you wrote choosecave() vs chooseCave().  You could try switching to
    # choose_cave to help keep these straight

    checkCave(caveNumber)

    print("Do you want to play again? (yes or no)")
    playAgain = input()
    if playAgain == "no":

        # print("Thanks for planing")
        print("Thanks for playing!")
        # you misspelled playing...

# I have to admit, it said '10 errors', but I'm only seeing 8.  Unless some of these count as multiples, that would explain the difference.  First time around, I remember conting 10, but I really don't see it this time...