from pymongo import MongoClient
import random
gameCollection = MongoClient('mongodb://localhost:27017/')['PSG']['games']
deb = random.randint(0, 75)
end = deb+15 
listID=list(gameCollection.find({},{"_id":1}))
sampleID=random.choice(listID)
sample=gameCollection.aggregate([
    { 
        "$match" : {
            "$and":[
                {
                    "Events.min": {
                        "$gte":deb
                    }
                },{
                    "Events.min":{
                        "$lte":end
                    }
                },
                {"_id":sampleID['_id']}
            ]
        }
    },
    { "$unwind" : "$Events" },
    { "$match" : {
        "$and":[
                {
                    "Events.min": {
                        "$gte":deb
                    }
                },{
                    "Events.min":{
                        "$lte":end
                    }
                }
            ]
        }
    }
  ])

sample["id"]=0
sample["away_team_id"]=0
sample["away_team_name"]="0"
sample["competition_id"]=0
sample["competition_name"]=""
sample["game_date"]=""
sample["home_team_id"]=1
sample["home_team_name"]="1"
sample["matchday"]=""
sample["period_1_start"]=""
sample["period_2_start"]=""
sample["season_id"]=0
sample["season_name"]=""
for event in sample:
    print(game['Events'])
    event["id"]=0
    event["event_id"]=0
    event["type_id"]=
    event["period_id"]=
    event["min"]=
    event["sec"]=
    event["player_id"]=
    event["team_id"]=
    event["outcome"]=
    event["x"]=0
    event["y"]=0
    event["timestamp"]=
    event["last_modified"]=
    event["version"]=
    for event in game['Events']:
        print(event)

