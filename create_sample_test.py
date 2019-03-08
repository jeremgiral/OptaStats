from pymongo import MongoClient
import random
from datetime import datetime  
from datetime import timedelta  

gameCollection = MongoClient('mongodb://localhost:27017/')['PSG']['games']
deb = random.randint(0, 30) 

['period_1_start','period_2_start']
listID=list(gameCollection.find({},{"_id":1}))
sampleID=random.choice(listID)
period=random.choice(['period_1_start','period_2_start'])
dateMatch=gameCollection.find_one({"_id":sampleID['_id']},{period:1,"_id":0})[period]
start=dateMatch+timedelta(minutes=deb)
end=dateMatch+timedelta(minutes=deb+15)
sample=list(gameCollection.find({ "_id":sampleID['_id']}))[0]
homeId=sample["home_team_id"]
awayId=sample["away_team_id"]
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
sample['Events']=[event for event in sample['Events'] if start <= event['timestamp'] <= end]

listJoueurs=list(set([event['player_id'] for event in sample['Events']]))
if '' in listJoueurs:
    listJoueurs.remove('')
joueurMystere=random.choice(listJoueurs)
for i,event in enumerate(sample['Events']):
    event["id"]=0
    event["event_id"]=0
    event["type_id"]="" if event["type_id"] in [140,141] else event["type_id"]
    event["period_id"]=""
    event["min"]=""
    event["sec"]=""
    event["player_id"]=1 if event["player_id"]==joueurMystere else 0
    event["team_id"]=1 if event["team_id"]==homeId else 0
    if i+10>=len(sample['Events']):
        event["outcome"]=""
    if i+10<len(sample['Events']):
        event["x"]=0
        event["y"]=0
    event["timestamp"]=""
    event["last_modified"]=""
    event["version"]=""
    for q in event['Qs']:
        q["id"]=0
        q["qualifier_id"]="" if q["qualifier_id"]  in [140,141] or i+10<len(sample['Events']) else q["qualifier_id"]
        q["value"]="" if i+10<len(sample['Events']) else q["value"]

sampleCollection = MongoClient('mongodb://localhost:27017/')['PSG']['sample']
sampleCollection.drop()
sampleCollection.insert_one(sample)
