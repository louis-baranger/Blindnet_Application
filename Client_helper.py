from os.path import dirname
from os.path import exists
from os import urandom

from pathlib import Path
from base64 import urlsafe_b64encode
import shutil
import requests

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# TODO: Change url to server URL
# TODO: Might make that a setting in the terminal interface
url = "http://localhost:8000"


def send():
    while True:
        print("Please, input f to send a file, s to send a string, or c to cancel:")
        choice = input()
        if choice == "f":
            print("Please, input the file path:")
            path = input()
            send_file(path)
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


def send_file(path):
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

    # TODO: determine what to do with that salt
    # TODO: more precisely, determine where to store it
    # TODO: needed for decryption
    # TODO: is it okay to store it with encrypted file on server?
    salt = encrypt_file(path, path_copy, password)

    file = {'file': open(path_copy, 'rb')}
    values = {'extension': p.suffix, 'salt': salt}
    r = requests.post(url, data=values, files=file)
    return


def encrypt_file(path, path_copy, password):
    print("TODO: Implement encrypt_file")
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
    return salt


def send_string():
    print("TODO: Implement send_string")
    return


def fetch():
    print("TODO: Implement fetch")
    return
