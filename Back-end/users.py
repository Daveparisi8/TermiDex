import json, sys, os, time
from models import LoginData, Pokemon

USERS_FILE = "users.json"

def load_users(filename=USERS_FILE):
    """Load existing users from disk (or return empty dict)."""
    if not os.path.isfile(filename):
        return {}
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    # data: { username_lower: {username, password_hash, pin}, … }
    return {u: LoginData.from_dict(d) for u, d in data.items()}

def save_users(users, filename=USERS_FILE):
    """Persist users dict to disk."""
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

    # everything’s valid—save it
    users[key] = new_user
    save_users(users)
    print(f"✅  Account for '{username}' created successfully!")

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

            # register_account()
        elif user_selection == 2:
            os.system('cls' if os.name=='nt' else 'clear')
            print("You chose: Log In")
            print("")
            time.sleep(2)
        elif user_selection == 3:
            print("You chose: Help")
            # show_help()
        elif user_selection == 4:
            print("You chose: About")
            # show_about()
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
        # loop back

def app():
    initialize_user()
    time.sleep(5)
    landing_menu()


if __name__ == "__main__":
    app()
