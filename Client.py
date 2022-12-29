# This is the driver. It is going to be a terminal interface.

import Client_helper as ch

settings = ch.SettingsClient

print("Welcome,")
while True:
    print("Please, input u to upload data, d to download data,"
          " q to quit, or s to change settings:")
    choice = input()
    print()
    if choice == "u":
        ch.send(settings)
    elif choice == "d":
        ch.fetch(settings)
    elif choice == "q":
        break
    elif choice == "s":
        settings.menu()
    else:
        print("Wrong input.")
        print("Please, input s to send, f to fetch, or q to quit:")
        print()

print("Thank you message")
