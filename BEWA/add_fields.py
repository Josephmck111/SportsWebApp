from pymongo import MongoClient
import random

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.WebApp
teams = db.teams

for team in teams.find():
    teams.update_one(
        { "_id" : team['_id'] },
        { 
            "$set" : { 
                "num_players" : random.randint(20, 50),
            } 
        }
    )
