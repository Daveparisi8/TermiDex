import json, sys, os, time
from models import LoginData, Pokemon
import services

USERS_FILE = "users.json"

def load_users(filename=USERS_FILE):
    if not os.path.isfile(filename):
        return {}
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {u: LoginData.from_dict(d) for u, d in data.items()}

def save_users(users, filename=USERS_FILE):
    with open(filename, "w", encoding="utf-8") as f:
        payload = {u: users[u].to_dict() for u in users}
        json.dump(payload, f, indent=2)

def register_account():
    users = load_users()

    username = input("Choose a username: ").strip()
    key = username.lower()
    if key in users:
        print("⚠️  That username is already taken.")
        return

    password = input("Enter a password: ")
    confirm = input("Confirm password: ")
    if password != confirm:
        print("⚠️  Passwords do not match.")
        return

    pin = input("Enter a 4-digit PIN: ")
    try:
        new_user = LoginData(username, password, pin)
    except ValueError as e:
        print(f"⚠️  {e}")
        return
    
    users[key] = new_user
    save_users(users)
    print(f"✅  Account for '{username}' created successfully!")

def do_login():
    users = load_users()

    username = input("Enter your account name: ").strip()
    key = username.lower()
    if key not in users:
        print(f"⚠️  No account found for '{username}'.")
        return

    user = users[key]
    for _ in range(3):
        pw = input("Enter your password: ")
        if user.check_password(pw):
            print(f"Welcome back, {user.username}!")
            user.reset_attempts()
            return
        else:
            user.increment_attempts()
            remaining = 3 - user.login_attempts
            print(f"Incorrect password. {remaining} attempt(s) left.")
            if user.is_locked:
                print("🔒  Too many failed attempts—account locked.")
                return

def initialize_user(): 
    os.system('cls' if os.name=='nt' else 'clear')
    print("Welcome to TermiDex!")
    print("A CLI for Pokémon fans that lets you:")
    print("  - Track how many Pokémon you’ve saved")
    print("  - See which ones you’ve yet to catch")
    print("  - Look up detailed data on any Pokémon")
    print("  - Log your championship teams")
    print("\nDeveloped by Dave Parisi.\n")
    print("")
    print("\nLoading main menu...\n")
def landing_menu():
    while True:
        os.system('cls' if os.name=='nt' else 'clear')
        print("Main Menu")
        print("---------")
        print("1. Register an Account")
        print("2. Log In")
        print("3. Help")
        print("4. About")
        print("5. Save and Exit")
        print("---------")

        try:
            user_selection = int(input("Input [1–5]: "))
        except ValueError:
            print("Please enter a number between 1 and 5.")
            time.sleep(1)
            continue

        if user_selection == 1:
            os.system('cls' if os.name=='nt' else 'clear')
            print("You chose: Register an Account")
            print("")
            time.sleep(2)
            
            register_account()

        elif user_selection == 2:
            os.system('cls' if os.name=='nt' else 'clear')
            print("You chose: Log In\n")
            time.sleep(1)
            do_login()


        elif user_selection == 3:
            print("You chose: Help")
            os.system('cls' if os.name=='nt' else 'clear')
            time.sleep(1)
            print("For all inquiries please reach out to david.parisi90@gmail.com")
            print("Returning to main menu...")
            time.sleep(5)
            continue

        elif user_selection == 4:
            print("You chose: About")
            print("TermiDex version: 1.01 beta release")
            input("\nPress Enter to return to the menu…")

        elif user_selection == 5:
            print("Saving critical data...")
            time.sleep(1)
            os.system('cls' if os.name=='nt' else 'clear')
            print("Main Menu")
            print("---------")
            print("1. Register an Account")
            print("2. Log In")
            print("3. Help")
            print("4. About")
            print("5. Save and Exit")
            print("---------")
            print("Goodbye!")
            break
        else:
            print("Invalid entry. Please try again.")

        input("\nPress Enter to return to the menu…")


def app():
    initialize_user()
    time.sleep(5)
    landing_menu()