import json, sys, os, time
from models import LoginData, Pokemon

#SERVICES FOR APP:::

# 1 ---------- Track how many Pokémon you’ve saved

###### User data is stored in .json files called caught_list and uncaught_list
###### Need menu to pull list of names and present names


CAUGHT_POKEMON = "caught_list.json"

def ensure_json_file_exists(filename = CAUGHT_POKEMON):
    if not os.path.isfile(filename):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('[]')
        print(f"Created empty JSON file at {filename}")


def load_caught_pokemon_func(filename=CAUGHT_POKEMON):
    if not os.path.isfile(filename):
        print(f"File does not exist: {filename}")
        return []

    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
        print(f"JSON file content:\n{content}")

        if not content.strip():
            print("JSON file is empty.")
            return []

        try:
            caught_data = json.loads(content)
            print("Raw loaded data:", caught_data)
            result = [Pokemon.from_dict(p) for p in caught_data]
            print("Deserialized data:", result)
            return result
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            return []


def save_caught_pokemon_func(pokemon_list, filename=CAUGHT_POKEMON):
    with open(filename, "w", encoding="utf-8") as f:
        payload = [p.to_dict() for p in pokemon_list]
        json.dump(payload, f, indent=2)



ensure_json_file_exists(CAUGHT_POKEMON)
print(load_caught_pokemon_func())


# 2 -------------------- Which ones you’ve yet to catch
# 3 ------------------------------ Look up detailed data on any Pokémon
# 4 ---------------------------------------- Log your championship teams