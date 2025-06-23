import json, sys, os, time
from models import LoginData, Pokemon
import users

#SERVICES FOR APP::

# 1 ---------- Track how many Pokémon you’ve saved

###### User data is stored in .json files called caught_list and uncaught_list
###### Need menu to pull list of names and present names

CAUGHT_POKEMON = "caught_list.json"

def load_caught_pokemon_func(filename = CAUGHT_POKEMON):
    if not os.path.isfile(filename):
        print("File does not exist.")
        return {}

    with open(filename, "r", encoding="utf-8") as f:
        caught_data = json.load(f)
        print("Raw loaded data:", caught_data)

    result = {u: LoginData.from_dict(d) for u, d in caught_data.items()}
    print("Deserialized data:", result)
    return result

def save_caught_pokemon_func(users, filename = CAUGHT_POKEMON):
    with open(filename, "w", encoding="utf-8") as f:
        payload = {u: users[u].to_dict() for u in users}
        json.dump(payload, f, indent=2)

print(load_caught_pokemon_func())


# 2 -------------------- Which ones you’ve yet to catch
# 3 ------------------------------ Look up detailed data on any Pokémon
# 4 ---------------------------------------- Log your championship teams