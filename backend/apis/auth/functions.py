from backend.constants import MINIMAL_PASSWORD_LENGTH
import re


def check_password_requirements(new_password, repeat_password):
    equal = new_password == repeat_password
    length = len(new_password) >= MINIMAL_PASSWORD_LENGTH
    lowercase = re.search("[a-z]", new_password)
    uppercase = re.search("[A-Z]", new_password)
    number = re.search("[0-9]", new_password)
    return all([equal, length, lowercase, uppercase, number])
