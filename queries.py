import json
import requests

from config import connection
<<<<<<< HEAD

# connection = pymysql.connect(
#     host="localhost",
#     user="root",
#     password="",
#     db="pokemon",
#     charset="utf8",
#     cursorclass=pymysql.cursors.DictCursor
# )
=======
>>>>>>> master

if connection.open:
    print("the connection is opened")


def get_data_from_json():
    with open("pokemon_data.json") as pokemon_data:
        data = json.load(pokemon_data)
    return data


def get_data_from_API():
    data = requests.get('https://pokeapi.co/api/v2')
    return data


def get_type_id(type_name):
    with connection.cursor() as cursor:
        type_query = 'SELECT type_name FROM types'
        cursor.execute(type_query)
        all_types = cursor.fetchall()
        all_types_names = []
        for type_element in all_types:
            all_types_names.append(type_element["type_name"])
        if type_name in all_types_names:
            q = "SELECT id FROM types WHERE type_name = (%s)"
            cursor.execute(q, type_name)
            id = cursor.fetchone()['id']
        else:
            cursor.execute('''SELECT COUNT(*) as c
                                    FROM types''')
            result = cursor.fetchone()
            id = result['c'] + 1
    return id


def insert_into_types(values):
    with connection.cursor() as cursor:
        type_query = 'SELECT type_name FROM types'
        cursor.execute(type_query)
        all_types = cursor.fetchall()
        all_types_names = []
        for type_element in all_types:
            all_types_names.append(type_element["type_name"])
        if values[1] not in all_types_names:
            type_query = 'INSERT INTO types values(%s, %s)'
            cursor.execute(type_query, values)
            connection.commit()
            return values[0]
        else:
            type_query = 'SELECT id FROM types WHERE type_name = (%s)'
            cursor.execute(type_query, values[1])
            type_id = cursor.fetchone()['id']
            return type_id


def insert_into_has_types(values):
    with connection.cursor() as cursor:
        q = 'SELECT * FROM has_types'
        cursor.execute(q)
        all_types = cursor.fetchall()
        print(all_types)
        all_types_names = []
        for type_element in all_types:
            all_types_names.append((type_element["pokemon_id"], type_element["type_id"]))
        if values not in all_types_names:
            has_type_query = 'INSERT INTO has_types values(%s, %s)'
            cursor.execute(has_type_query, values)
            connection.commit()


def add_pokemon(pokemon):
    try:
        with connection.cursor() as cursor:
            query = 'INSERT INTO pokemon VALUES (%s,%s,%s,%s)'
            values = (pokemon['id'], pokemon['name'],
                      pokemon['height'], pokemon['weight'])
            cursor.execute(query, values)
            connection.commit()
            if type(pokemon['type']) is str:
                type_id = get_type_id(pokemon['type'])
                type_values = (type_id, pokemon['type'])
                type_id = insert_into_types(type_values)
                has_type_values = (pokemon['id'], type_id)
                insert_into_has_types(has_type_values)
            else:
                for t in pokemon['type']:
                    cursor.execute('''SELECT id 
                                    FROM types
                                    WHERE type = %s'''
                                   , t)
                    result = cursor.fetchall()
                    type_id = get_type_id(t)
                    if result == 'no data':
                        type_values = (type_id, t)
                        type_id = insert_into_types(type_values)
                        has_type_values = (pokemon['id'], type_id)
                        insert_into_has_types(has_type_values)
            return True
    except:
        print("Error: Failed to add a new pokemon")
        return False


def insert_to_database():
    data = get_data_from_json()
    trainers = []
    types = []
    for pokemon in data:
        try:
            with connection.cursor() as cursor:
                add_pokemon(pokemon)

                query_trainer = 'INSERT INTO trainer VALUES (%s,%s,%s)'

                query_owned_by = 'INSERT INTO owned_by VALUES (%s,%s)'

                for trainer in pokemon['ownedBy']:
                    if trainer not in trainers:
                        trainers.append(trainer)
                        trainer_id = len(trainers)
                        values_trainer = (trainer_id, trainer['name'], trainer['town'])
                        cursor.execute(query_trainer, values_trainer)
                        connection.commit()
                    else:
                        counter = 1
                        for tr in trainers:
                            if tr == trainer:
                                trainer_id = counter
                                break
                            counter += 1
                    values_owned_by = (pokemon['id'], trainer_id)
                    cursor.execute(query_owned_by, values_owned_by)
                    connection.commit()
        except:
            print("Error: Failed to insert data into DB")


def heaviest_pokemon():
    try:
        with connection.cursor() as cursor:
            cursor.execute('''SELECT name AS heaviest 
                            FROM pokemon 
                            WHERE weight = (
                                SELECT MAX(weight) 
                                FROM pokemon)''')
            result = cursor.fetchall()
            return result[0]['heaviest']
    except:
        print("Error: Failed to select the heaviest pokemon")


def find_by_type(type):
    try:
        with connection.cursor() as cursor:
            cursor.execute('''SELECT p.name 
                    FROM pokemon p, has_types h, types t 
                    WHERE p.id = h.pokemon_id
                    AND  h.type_id = t.id
                    AND t.type_name = (%s)''', type)
            pokemons = cursor.fetchall()
            pokemons_names = []
            for i in pokemons:
                pokemons_names.append(i['name'])
            return pokemons_names
    except:
        print("Error: Failed to find pokemon by type")


def find_owners(pokemon_name):
    try:
        with connection.cursor() as cursor:
            cursor.execute('''SELECT t.name 
                            FROM pokemon p, owned_by o, trainer t 
                            WHERE p.id = o.pokemon_id 
                            AND t.id = o.trainer_id 
                            AND p.name = %s''', pokemon_name)
            result = cursor.fetchall()
            name_list = []
            for name in result:
                name_list.append(name['name'])
            return name_list
    except:
        print("Error: Failed to find owners to this pokemon")


def find_roster(trainer_name):
    try:
        with connection.cursor() as cursor:
            cursor.execute('''SELECT id 
                            FROM trainer 
                            WHERE name = (%s)'''
                           , trainer_name)
            trainer_id = cursor.fetchall()[0]['id']
            cursor.execute('''SELECT pokemon_id 
                            FROM owned_by 
                            WHERE trainer_id = (%s)'''
                           , trainer_id)
            pokemon_ids = cursor.fetchall()
            pokemons = []
            for i in pokemon_ids:
                cursor.execute('''SELECT name 
                                FROM pokemon 
                                WHERE id = (%s)'''
                               , i['pokemon_id'])
                pokemons.append(cursor.fetchone())
            pokemon_names = []
            for i in pokemons:
                pokemon_names.append(i['name'])
            return pokemon_names
    except:
        print("Error: Failed to find pokemons of this trainer")


def finds_most_owned():
    try:
        with connection.cursor() as cursor:
            cursor.execute('''SELECT pokemon_id
                            FROM (
                            SELECT pokemon_id, COUNT(*) as count
                            FROM owned_by
                            GROUP BY pokemon_id) as A
                            WHERE count >= ALL(SELECT  COUNT(*)
                            FROM owned_by
                            GROUP BY pokemon_id)''')
            result = cursor.fetchall()
            most_owned = []
            for pokemon in result:
                most_owned.append(pokemon['pokemon_id'])
            return most_owned
    except:
        print("Error: Failed to find the most owned pokemon")


def delete_pokemon_sql(pokemon_id):
    try:
        with connection.cursor() as cursor:
            query = 'DELETE FROM pokemon WHERE id = (%s)'
            values = (pokemon_id)
            cursor.execute(query, values)
            connection.commit()
            return "Deleted pokemon successfully"
    except:
        print("Error: Failed to delete a pokemon")


def select_pokemon_id(pokemon_name):
    with connection.cursor() as cursor:
        cursor.execute('''SELECT id 
                FROM pokemon 
                WHERE name = %s'''
                       , pokemon_name)
        result = cursor.fetchone()
        return result['id']


def select_trainer_id(trainer_name):
    with connection.cursor() as cursor:
        cursor.execute('''SELECT id 
                        FROM trainer 
                        WHERE name = %s'''
                       , trainer_name)
        result = cursor.fetchone()
        return result['id']


def select_trainers(pokemon_id):
    with connection.cursor() as cursor:
        cursor.execute('''SELECT trainer_id
                        FROM owned_by
                        WHERE pokemon_id = %s'''
                       , pokemon_id)
        trainers = cursor.fetchall()
        return trainers


<<<<<<< HEAD
def update_pokemon_in_owned_by(evolved_pokemon, pokemon_id, trainer_id):
    with connection.cursor() as cursor:
        values = (evolved_pokemon, pokemon_id, trainer_id)
        query = '''UPDATE owned_by
                SET pokemon_id = %s
                WHERE pokemon_id = %s 
                AND trainer_id = %s'''
        cursor.execute(query, values)

# def evolve(pokemon_name, trainer_name):
#     # try:
#         url = 'https://pokeapi.co/api/v2/pokemon/{}'.format(pokemon_name)
#         pokemon_info = requests.get(url, verify=False)
#         a= pokemon_info.json()
#         # pokemon_info = http.request('GET', url).json()
#         species_url = pokemon_info['species']['url']
#         species_info = requests.get(species_url, verify=False).json()
#         # species_info = http.request('GET', species_url).json()
#         evolution_chain_url = species_info['evolution_chain']['url']
#         evolution_chain_info = requests.get(evolution_chain_url, verify=False)
#         # evolution_chain_info = http.request('GET', evolution_chain_url)
#         chain_item = evolution_chain_info['chain']
#         current_form = chain_item['evolves_to']
#         next_form = current_form['evolves_to']
#
#         while next_form['evolves_to']:
#             current_form = next_form[:]
#             next_form = current_form['evolves_to'][:]
#         evolved_pokemon = current_form['species']['name']
#         with connection.cursor() as cursor:
#             cursor.execute('''SELECT id
#                     FROM pokemon
#                     WHERE name = %s'''
#                     , pokemon_name)
#             result = cursor.fetchone()
#             pokemon_id = result['id']
#             cursor.execute('''SELECT id
#                             FROM trainer
#                             WHERE name = %s'''
#                            , trainer_name)
#             result = cursor.fetchone()
#             trainer_id = result['id']
#             cursor.execute('''SELECT trainer_id
#                                     FROM owned_by
#                                     WHERE pokemon_id = %s'''
#                                     , evolved_pokemon)
#             trainers = cursor.fetchall()
#             trainers_id = []
#             for trainer in trainers:
#                 trainers_id.append(trainer['trainer_id'])
#             if trainer_id not in trainers_id:
#                 evolve_query = '''UPDATE owned_by
#                             SET pokemon_id = %s
#                             WHERE pokemon_id = %s
#                             AND trainer_id = %s'''
#                 evolve_values = (evolved_pokemon, pokemon_id, trainer_id)
#                 cursor.execute(evolve_query, evolve_values)
#             else:
#                 print("evolved pokemon already exist")
#     # except:
#     #     print("Error: Failed to update this pokemon of this trainer")
#
# # evolve('charmander', 'Jasmine')
#
# # url = 'https://pokeapi.co/api/v2/pokemon/{}'.format('charmander')
# # pokemon_info = requests.get(url, verify=False).json()
# url = 'https://pokeapi.co/api/v2/pokemon/{}'.format('charmander')
# pokemon_info = requests.get(url, verify=False)
# a=pokemon_info.json()
# def update_types_for_pokemon(pokemon_name):
#     res = requests.get('https://pokeapi.co/api/v2/pokemon/{}'.format(pokemon_name), verify=False).json()
#     types = res["types"]
#     pokemon_id = res["id"]
#     # try:
#     print(types)
#     types_names = []
#     for type in types:
#         types_names.append(type["type"]["name"])
#     print("types_names {}".format(types_names))
#     for type in types_names:
#         type_id = get_type_id(type)
#         type_id = insert_into_types((+type_id, type))
#         insert_into_has_types((pokemon_id, type_id))
#         return "Updated pokemons type successfully"
#     # except:
#     #     print("Error: Failed to update types of pokemon")
=======
def update_pokemon_in_owned_by(evolved_pokemon_id, pokemon_id, trainer_id):
    try:
        with connection.cursor() as cursor:
            values = (evolved_pokemon_id, pokemon_id, trainer_id)
            query = '''UPDATE owned_by
                    SET pokemon_id = %s
                    WHERE pokemon_id = %s 
                    AND trainer_id = %s'''
            cursor.execute(query, values)
            connection.commit()
    except:
        print("Error: Failed to update")
>>>>>>> master
