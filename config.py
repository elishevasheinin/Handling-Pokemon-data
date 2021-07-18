import pymysql

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    db="pokemon",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)

port = 5000

url = 'https://pokeapi.co/api/v2/pokemon/'