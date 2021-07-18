from flask import Flask, Response, request

from queries import *
from client import evolve, update_types_for_pokemon
from config import port

app = Flask(__name__)

'''
access this route with the link 'localhost:5000/get_pokemons/<trainer_name>'
where the response will be all the pokemons owned by trainer_name
'''
@app.route('/get_pokemons/<trainer_name>', methods=['GET'])
def get_pokemons_of_trainer(trainer_name):
    res = find_roster(trainer_name)
    return Response("{}".format(res))


'''
access this route with the link 'localhost:5000/get_trainers/<pokemon_name>'
where the response will be all the trainers that owen pokemon_name
'''
@app.route('/get_trainers/<pokemon_name>', methods=['GET'])
def get_trainers_of_pokemon(pokemon_name):
    res = find_owners(pokemon_name)
    return Response("{}".format(res))


'''
access this route with the link 'localhost:5000/new_pokemon'
send params in body {'name', 'height', 'weight'} 
'''
@app.route('/new_pokemon', methods=['POST'])
def new_pokemon():
    pokemon_details = request.get_json()
    added = add_pokemon(pokemon_details)
    if added:
        return Response("Added a new pokemon successfully")
    return Response("Addition failed")


'''
access this route with the link 'localhost:5000/pokemon_by_type/<type>'
where the response will be all the pokemons names who are have type
'''
@app.route('/pokemon_by_type/<type>', methods=['GET'])
def get_pokemon_by_type(type):
    res = find_by_type(type)
    return Response("{}".format(res))


'''
access this route with the link 'localhost:5000/delete_pokemon/<pokemon_id>'
will delete pokemon whose id was sent from the DB
'''
@app.route('/delete_pokemon/<pokemon_id>', methods=['DELETE'])
def delete_pokemon(pokemon_id):
    res = delete_pokemon_sql(pokemon_id)
    return Response("{}".format(res))


'''
access this route with the link 'localhost:5000/update_types/<pokemon_name>'
will update the types from pokemon from the API
'''
@app.route('/update_types/<pokemon_name>', methods=['POST'])
def update_types(pokemon_name):
    res = update_types_for_pokemon(pokemon_name)
    return Response("{}".format(res))


'''
access this route with the link 'localhost:5000/evolve_pokemon/<pokemon_name>/<trainer_name>'
will evolve the pokemon trained by trainer_name
'''
@app.route('/evolve_pokemon/<pokemon_name>/<trainer_name>', methods=['PATCH'])
def evolve_pokemon(pokemon_name, trainer_name):
    succeeded = evolve(pokemon_name, trainer_name)
    if succeeded:
        return Response("Evolved pokemon {} of {} successfully".format(pokemon_name, trainer_name))
    return Response("Evolution failed")


if __name__ == '__main__':
    app.run(port=port)
