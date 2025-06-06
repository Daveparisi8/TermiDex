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
import array
import random
import math
import json
import sys
import os

### National pokedex. Contains all pokemon

### Application login / Setup
class loginData:
    def __init__(self, username, password, confirm_password, pin):
        self.username = username
        self.password = password
        self.confirm_password = confirm_password
        self.pin = pin
        self.login_attempts = 0
        self.is_locked = False

    def __str__(self):
        return f"Username: {self.username}, Password: {self.mask_password()}, PIN: {self.pin}, Locked: {self.is_locked}"
    
    def __repr__(self):
        return self.__str__()

    def is_valid_password(self):
        return self.password == self.confirm_password

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
#Classes
    @classmethod
    def from_dict(cls, data):
        return cls(data["username"], data["password"], data["password"], data["pin"])
class userData:
    def __init__(self,captureCount,remainCount):
        self.captureCount = captureCount
        self.remainCount = remainCount

    def display(self):
        print(f"Pokémon quantity caught: {self.captureCount}")
        print(f"Pokémon quantity remaining: {self.remainCount} ")
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

def get_valid_integer(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter an integer.")
def login():

    while True:   
        print("")
        print("-Main Menu-")
        print("1.) Log In")
        print("2.) New User")
        print('3.) Exit')
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
                        fav_pk = input("Optional: who is your favorite Pokemon? ").strip().lower()

                        match = next((p for p in national_pokedex if p["name"]["english"].lower() == fav_pk), None)
                        
                        if match:
                            print(json.dumps(match, indent=2))
                        else:
                            print(f"{fav_pk.title()} not found in the Pokédex.")                        
                    break
            break
def catch_false():
    for pokemon in national_pokedex:
        if not pokemon.get("caught", False):
            print(pokemon["name"]["english"])
def catch_true():
    for pokemon in national_pokedex:
        if pokemon.get("caught", False):
            print(pokemon["name"]["english"])



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



new_user()