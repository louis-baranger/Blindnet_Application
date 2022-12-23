# This is the driver. It is going to be a terminal interface.

import Client_helper as ch

print("Welcome message")

while True:
    print("Would you like to send data, fetch data, or quit?")
    choice = input()
    if choice == "s":
        ch.send()
    elif choice == "f":
        ch.fetch()
    elif choice == "q":
        break
    else:
        print("Wrong input.")
        print("Please, input s to send, f to fetch, or q to quit:")
        print()

print("Thank you message")
