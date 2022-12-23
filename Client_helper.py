from os.path import dirname
from os.path import exists
from os import urandom
from os import remove

from pathlib import Path
from base64 import urlsafe_b64encode
import shutil
import requests

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# TODO: Change url to server URL
# TODO: Might make that a setting in the terminal interface
# TODO: Could also include timeout setting
url = "http://localhost:8000"


def send():
    while True:
        print("Please, input f to send a file, s to send a string, or c to cancel:")
        choice = input()
        if choice == "f":
            print("Please, input the file path:")
            path = input()
            send_file(path, "file")
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


def send_file(path, type_of_send):
    p = Path(path)
    if not (p.is_file()):
        print("Invalid path.")
        return
    print("Please, input your password:")
    password = input().encode('ascii')

    directory = dirname(path)
    # TODO: This will not work with multiple file extensions e.g. ".tar.gz"
    path_copy = directory + '/' + p.stem + "_copy" + p.suffix

    i = 0
    while exists(path_copy):
        path_copy = directory + '/' + p.stem + "_copy_" + str(i) + p.suffix
        i += 1

    salt = encrypt_file(path, path_copy, password)

    file = {'file': open(path_copy, 'rb')}
    values = {'extension': p.suffix, 'salt': salt, 'type': type_of_send, 'name': p.stem}

    r = requests.post(url, files=file, headers=values)

    if r.status_code == 200:
        remove(path_copy)
        print("Successfully encrypted and sent " + str(type_of_send) + " to server.")
        print("Here is your Unique ID:")
        print(r.content.decode('ascii'))
    else:
        print("Error during file transmission to server.")
        print("Error code: " + str(r.status_code))
        remove(path_copy)
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
    path_to_encrypt = "temp.txt"

    i = 0
    while exists(path_to_encrypt):
        path_to_encrypt = "temp_" + str(i) + ".txt"

    f = open(path_to_encrypt, "wb")
    f.write(text)
    f.close()

    send_file(path_to_encrypt, "string")
    return


def fetch():
    print("TODO: Implement fetch")
    return
