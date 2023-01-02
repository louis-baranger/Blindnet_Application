from os import getcwd
from os.path import exists


def menu(settings):
    print('Please, press d to use default settings, c to use custom settings, or q to quit:')
    choice = input()
    print()
    while True:
        if choice == 'd':
            return True
        elif choice == 'c':
            settings.custom_settings()
            return True
        elif choice == 'q':
            print('Thank you for using this application.')
            return False
        else:
            print('Invalid choice')
            print('Please, press d to use default settings, c to use custom settings, or q to quit:')


class SettingsServer:

    def custom_settings(self):

        choice = 0
        while choice != 4:
            print("What would you like to change?")
            print("1. Storage Folder")
            print("2. Host")
            print("3. Port")
            print("4. Exit settings and start server")
            try:
                choice = int(input())
            except ValueError:
                print("Invalid input.")
            if choice == 1:
                print("Storage Folder:")
                temp_path = input()
                if exists(temp_path):
                    self.storage_folder = temp_path
                else:
                    print("Invalid path")

            elif choice == 2:
                print("Host:")
                self.host = input()

            elif choice == 3:
                print("Port:")
                self.port = input()

    storage_folder = getcwd()
    host = ''
    port = 8000

