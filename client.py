import requests
from config import url
from queries import get_type_id, insert_into_types, insert_into_has_types,\
                    select_pokemon_id, select_trainer_id, select_trainers, \
                    update_pokemon_in_owned_by


def update_types_for_pokemon(pokemon_name):
    res = requests.get(url + pokemon_name, verify=False).json()
    types = res["types"]
    pokemon_id = res["id"]
    try:
        types_names = []
        for type in types:
            types_names.append(type["type"]["name"])
        for type in types_names:
            type_id = get_type_id(type)
            type_id = insert_into_types((type_id, type))
            insert_into_has_types((pokemon_id, type_id))
            return "Updated pokemon's type successfully"
    except:
        print("Error: Failed to update types of pokemon")


def evolve(pokemon_name, trainer_name):
    try:
        api_url = url + pokemon_name
        pokemon_info = requests.get(api_url, verify=False).json()
        species_url = pokemon_info['species']['url']
        species_info = requests.get(species_url, verify=False).json()
        evolution_chain_url = species_info['evolution_chain']['url']
        evolution_chain_info = requests.get(evolution_chain_url, verify=False).json()
        chain_item = evolution_chain_info['chain']
        current_form = chain_item['evolves_to'][0]
        next_form = current_form['evolves_to'][0]

        while next_form['evolves_to']:
            current_form = next_form[:]
            next_form = current_form['evolves_to'][:]
        evolved_pokemon = current_form['species']['name']

        pokemon_id = select_pokemon_id(pokemon_name)
        trainer_id = select_trainer_id(trainer_name)
        evolved_pokemon_id = select_pokemon_id(evolved_pokemon)
        trainers = select_trainers(evolved_pokemon)

        trainers_id = []
        for trainer in trainers:
            trainers_id.append(trainer['trainer_id'])
        if trainer_id not in trainers_id:
            update_pokemon_in_owned_by(evolved_pokemon_id, pokemon_id, trainer_id)
            return True
        print("evolved pokemon already exist")
        return False
    except:
        print("Error: Failed to update this pokemon of this trainer")


evolve('charmander', 'Jasmine')