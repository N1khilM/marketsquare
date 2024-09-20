def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


# utils.py

import random

def generate_otp():
    return random.randint(100000, 999999)
