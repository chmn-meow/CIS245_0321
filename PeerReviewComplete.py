# Peer Review Author: Jayson Davidson
# Peer Review Date: 06-Dec-20

import random
import time


def display_intro():
    intro = "You are in a land full of dragons. In front of you,\nyou see two caves. In one cave, the dragon is friendly\nand will share his treasure with you. The other dragon\nis greedy and hungry, and will eat you on sight."
    print(f"{intro}\n")


def choose_cave():
    cave = None
    while cave != 1 and cave != 2:
        print("Which cave will you go into? (1 or 2)")
        cave = int(input())
    return cave


def check_cave(chosen_cave):
    print("You approach the cave...")
    # sleep for 2 seconds
    time.sleep(2)
    print("It is dark and spooky...")
    # sleep for 2 seconds
    time.sleep(2)
    print("A large dragon jumps out in front of you! He opens his jaws and...\n")
    # sleep for 2 seconds
    time.sleep(2)
    frinedly_cave = random.randint(1, 2)

    if chosen_cave == frinedly_cave:
        print("Gives you his treasure!")
    else:
        print("Gobbles you down in one bite!")


play_again = "yes"
while play_again == "yes" or play_again == "y":
    display_intro()
    cave_number = choose_cave()
    check_cave(cave_number)

    print("Do you want to play again? (yes or no)")
    play_again = input()
print("Thanks for playing!")