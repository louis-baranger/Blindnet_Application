from os.path import exists
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import shutil


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
    if not(exists(path)):
        print("Invalid path.")
        return
    print("Please, input your password:")
    password = input()
    path_encrypted = encrypt_file(path)

    return


def encrypt_file(path):
    print("TODO: Implement encrypt_file")
    encrypted_file = "temp"
    # create copy, encrypt

    # return path to encrypted file
    return encrypted_file


def send_string():
    print("TODO: Implement send_string")
    return


def fetch():
    print("TODO: Implement fetch")
    return
