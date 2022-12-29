from os.path import dirname
from os.path import exists
from os import urandom
from os import remove
from os import getcwd

from pathlib import Path
from base64 import b64encode
from base64 import b64decode
from base64 import urlsafe_b64encode

import cryptography.fernet
import requests

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def send(settings):
    while True:
        print("Please, input f to send a file, s to send a string, or c to cancel:")
        choice = input()
        print()
        if choice == "f":
            print("Please, input the file path:")
            path = input()
            print()
            send_file(settings, path, "file")
            break
        elif choice == "s":
            send_string()
            break
        elif choice == "c":
            print("Send request cancelled.")
            break
        else:
            print("Wrong input.")
            continue

    return


def send_file(settings, path, type_of_send):
    p = Path(path)
    if not (p.is_file()):
        print("Invalid path.")
        return
    print("Please, input your password:")
    password = input().encode('ascii')
    print()

    directory = dirname(path)
    # TODO: This will not work with multiple file extensions e.g. ".tar.gz"
    path_copy = directory + '/' + p.stem + "_copy" + p.suffix

    i = 0
    while exists(path_copy):
        path_copy = directory + '/' + p.stem + "_copy_" + str(i) + p.suffix
        i += 1

    salt = encrypt_file(path, path_copy, password)

    file = {'file': open(path_copy, 'rb')}

    # Transforms salt into string to avoid errors during transmission
    salt = b64encode(salt).decode('utf-8')
    # Command to run to decode:
    # salt = b64decode(salt.encode('utf-8'))
    values = {'extension': p.suffix, 'salt': salt, 'type': type_of_send, 'name': p.stem}

    try:
        r = requests.post(settings.url, files=file, headers=values)
    except:
        print("Error during file transmission to server.")
        remove(path_copy)
        return

    remove(path_copy)
    print("Successfully encrypted and sent " + str(type_of_send) + " to server.")
    print("Here is your Unique ID:")
    print(r.content.decode('ascii'))
    return


def encrypt_file(path, path_copy, password):
    # Creates a key derivation function using values suggested by the cryptography library
    salt = urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )

    key = urlsafe_b64encode(kdf.derive(password))

    fernet = Fernet(key)
    original = open(path, 'rb').read()
    encrypted = fernet.encrypt(original)

    encrypted_copy = open(path_copy, 'wb')
    encrypted_copy.write(encrypted)
    encrypted_copy.close()
    return salt


def send_string():
    print("Please, input the string:")
    text = input().encode('ascii')
    print()
    path_to_encrypt = "temp.txt"

    i = 0
    while exists(path_to_encrypt):
        path_to_encrypt = "temp_" + str(i) + ".txt"

    f = open(path_to_encrypt, "wb")
    f.write(text)
    f.close()

    send_file(path_to_encrypt, "string")
    return


def fetch(settings):
    print("Please, input the Unique ID of the file:")
    unique_id = input()
    print()

    values = {'id': str(unique_id)}
    try:
        r = requests.get(settings.url, headers=values)
    except:
        print('Error during connection to server.')
        return

    if r.status_code == 201:
        print("File does not exist on server.")
        return

    print("Please, input your password:")
    password = input().encode('ascii')
    print()
    path = decrypt_file(settings, r, password)

    # path is N/A if there is an error with decryption (most likely due to wrong password input)
    if path == 'N/A':
        return

    type_send = r.headers['type_send']
    if type_send == "file":
        print("File successfully downloaded.")
        print("File is stored at:", path)
    else:
        file = open(path, 'rb')
        print("String is:")
        print(file.read().decode('ascii'))
        file.close()

    return


def decrypt_file(settings, request, password):
    path = settings.download_path + '/' + request.headers['name'] + request.headers['extension']

    i = 0
    while exists(path):
        path = settings.download_path + '/' + request.headers['name'] + '_' + str(i) + request.headers['extension']
        i += 1
    file = open(path, 'wb')

    salt = b64decode(request.headers['salt'].encode('utf-8'))
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )

    key = urlsafe_b64encode(kdf.derive(password))

    fernet = Fernet(key)
    try:
        file.write(fernet.decrypt(request.content))
        file.close()
        return path
    except cryptography.fernet.InvalidToken:
        file.close()
        print('Error during decryption most likely due to a wrong password.')
        return 'N/A'


class SettingsClient:

    def menu(self):
        choice = 0
        while choice != 3:
            print("What would you like to change?")
            print("1. Server URL")
            print("2. Download path")
            print("3. Exit settings")
            choice = int(input())
            if choice == 1:
                print("URL:")
                self.url = input()
            elif choice == 2:
                print("Download path:")
                temp_path = input()
                if exists(temp_path):
                    self.download_path = temp_path
                else:
                    print("Invalid path")

        return

    url = 'http://localhost:8000'
    download_path = getcwd()
