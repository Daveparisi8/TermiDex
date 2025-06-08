# quu..__
#  $$$b  `---.__
#   "$$b        `--.                          ___.---uuudP
#    `$$b           `.__.------.__     __.---'      $$$$"              .
#      "$b          -'            `-.-'            $$$"              .'|
#        ".                                       d$"             _.'  |
#          `.   /                              ..."             .'     |
#            `./                           ..::-'            _.'       |
#             /                         .:::-'            .-'         .'
#            :                          ::''\          _.'            |
#           .' .-.             .-.           `.      .'               |
#           : /'$$|           .@"$\           `.   .'              _.-'
#          .'|$u$$|          |$$,$$|           |  <            _.-'
#          | `:$$:'          :$$$$$:           `.  `.       .-'
#          :                  `"--'             |    `-.     \
#         :##.       ==             .###.       `.      `.    `\
#         |##:                      :###:        |        >     >
#         |#'     `..'`..'          `###'        x:      /     /
#          \                                   xXX|     /    ./
#           \                                xXXX'|    /   ./
#           /`-.                                  `.  /   /
#          :    `-  ...........,                   | /  .'
#          |         ``:::::::'       .            |<    `.
#          |             ```          |           x| \ `.:``.
#          |                         .'    /'   xXX|  `:`M`M':.
#          |    |                    ;    /:' xXXX'|  -'MMMMM:'
#          `.  .'                   :    /:'       |-'MMMM.-'
#           |  |                   .'   /'        .'MMM.-'
#           `'`'                   :  ,'          |MMM<
#             |                     `'            |tbap\
#              \                                  :MM.-'
#               \                 |              .''
#                \.               `.            /
#                 /     .:::::::.. :           /
#                |     .:::::::::::`.         /
#                |   .:::------------\       /
#               /   .''               >::'  /
#               `',:                 :    .'
#                                    `:.'
###############
### Imports ###
###############
              #   #
import json   #
import sys    #
import os     #
import hashlib#
              #
###############


### Application login / Setup

class loginData:
    def __init__(self, username, password, confirm_password, pin):
        self.username = username
        self.password = password
        self.pin = pin
        self.login_attempts = 0
        self.is_locked = False

    def __str__(self):
        return f"Username: {self.username}, Password: {self.mask_password()}, PIN: {self.pin}, Locked: {self.is_locked}"
    
    def __repr__(self):
        return self.__str__()
    import hashlib, os

    def _hash_password(self, raw):
        salt = os.urandom(16)
        key = hashlib.pbkdf2_hmac('sha256', raw.encode(), salt, 100_000)
        return salt + key

    def check_password(self, raw):
        salt, key = self.password[:16], self.password[16:]
        test = hashlib.pbkdf2_hmac('sha256', raw.encode(), salt, 100_000)
        return test == key

    def mask_password(self):
        return '*' * len(self.password)

    def increment_attempts(self):
        self.login_attempts += 1
        if self.login_attempts >= 3:
            self.is_locked = True

    def reset_attempts(self):
        self.login_attempts = 0
        self.is_locked = False

    def display(self):
        print(f"Username: {self.username}")
        print(f"Password: {self.mask_password()}")
        print(f"PIN: {self.pin}")
        print(f"Locked: {self.is_locked}")
        
    def to_dict(self):
        return {
        "username": self.username,
        "password": self.password,
        "pin": self.pin
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(data["username"], data["password"], data["password"], data["pin"])
    
    @property
    def is_locked(self):
        return self.login_attempts >= 3
    
class Pokemon:
    def __init__(self, name, types, evolves_to, caught=False):
        self.name = name
        self.types = types
        self.evolves_to = evolves_to
        self.caught = caught

    def to_dict(self):
        return {
            "name": self.name,
            "type": self.types,
            "evolves_to": self.evolves_to,
            "caught": self.caught
        }
    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            types=data["type"],
            evolves_to=data.get("evolves_to", []),
            caught=data.get("caught", False)
        )
    
    def __repr__(self):
        status = "✓" if self.caught else "✗"
        return f"<Pokemon {self.name} ({'/'.join(self.types)}) {status}>"
    
    def catch(self):
        if not self.caught:
            self.caught = True
        else:
            raise RuntimeError(f"{self.name} already caught!")
            
    def release(self):
        self.caught = False

def get_valid_integer(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter an integer.")
def login():

    while True:   
        print("")
        print("-CLI Menu-")
        print("1. Log In")
        print("2. New User")
        print('3. Exit')
        print("")

        menu_choice = get_valid_integer("Choose an option: ")

        if menu_choice == 1:
            while True:
                print("-Login-")
                input_username = input("Enter Username (Case insensitive): ").strip().lower()

                if input_username in users:
                    print("User found.")

                    logged_user = users[input_username]
                    logged_user.reset_attempts()

                    while not logged_user.is_locked:
                        input_password = input("Enter Password (Case sensitive): ")

                        if input_password == logged_user.password:
                            print("Password Correct. Access granted.")
                            break
                        else:
                            logged_user.increment_attempts()
                            remaining_attempts = 3 - logged_user.login_attempts
                            if not logged_user.is_locked:
                                print(f"Incorrect Password. {remaining_attempts} attempts remaining.")
                            else:
                                print("Too many failed attempts. Account locked. Exiting program.")
                                sys.exit()
                else:
                    print("User not found. Please try again.")
                    break
        if menu_choice == 2:
            new_user()
        elif menu_choice == 3:
            print("Exiting program. Goodbye!")
            sys.exit()

def new_user():
    print("-Create New Account-")
    while True:
        username = input("Select a user name: ")
        if username in users:
            print("User name is taken. Please select a new user name.")
        else:
            password = input("Select a password: ")
            c_password = input ("confirm your password: ")
            if password == c_password:
                while True:
                    try:
                        pin = input("Enter a 4-digit PIN: ")
                    except ValueError:
                        print("Invalid PIN selection. Please try again.")

                    c_pin = input("Confirm 4-digit PIN: ")
                    if pin == c_pin:
                        print("Login successful.")
                        
                    break
            break
def catch_check(name):
    for p in pokemon_list:
        if p.name.lower() == name.lower():
            return p.caught
    return False
def ensure_list_files():


    for filename in ('caught_list.txt', 'uncaught_list.txt'):
        if not os.path.isfile(filename):
            with open(filename, 'w', encoding='utf-8'):
                pass

def mainApp():
    while True:
        login()
        # if login() == False:
        #     new_user()




ensure_list_files()

try:
    with open("users.json", "r") as f:
        data = json.load(f)
        users = {u: loginData.from_dict(d) for u, d in data.items()}
except FileNotFoundError:
    users = {}

if os.path.exists("pokemon_data.json"):
    with open("pokemon_data.json", "r", encoding="utf-8") as f:
        national_pokedex = json.load(f)
else:
    with open("pokedex.json", "r", encoding="utf-8") as f:
        national_pokedex = json.load(f)

pokemon_list = []
for p in national_pokedex:
    pokemon = Pokemon(
        name=p["name"]["english"],
        types=p["type"],
        evolves_to=p.get("evolution", {}).get("next", []),
        caught=p.get("caught", False)
    )
    pokemon_list.append(pokemon)

users = {}
user = loginData("Ash", "pikachu123", "pikachu123", 1234)
users[user.username.lower()] = user

mainApp()
