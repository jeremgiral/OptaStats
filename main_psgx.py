import xmltodict
import os
from pymongo import MongoClient
import time
class Equipe:
    def __init__(self,country,country_id,country_iso,region_id,region_name,short_club_name,uID,web_address,Founded,Name,SYMID,StadiumuID,Capacity,StadiumName,TeamKits,Players,TeamOfficials):
        self.country=country
        self.country_id=country_id
        self.country_iso=country_iso
        self.region_id=region_id
        self.region_name=region_name
        self.short_club_name=short_club_name
        self.uID=uID
        self.web_address=web_address
        self.Founded=Founded
        self.Name=Name
        self.SYMID=SYMID
        self.StadiumuID=StadiumuID
        self.StadiumName=StadiumName
        self.Capacity=Capacity
        self.TeamKits=TeamKits
        self.Players=Players
        self.TeamOfficials=TeamOfficials
    def __repr__(self):
        return str(vars(self))   

class Joueur:
    def __init__(self,uID,Name,Position,Stat):
        self.uID=uID
        self.Name=Name
        self.Position=Position
        self.Stat=Stat
    def __repr__(self):
        return str(vars(self))

class KitEquipe:
    def __init__(self,uid,colour1,colour2,type):
        self.uid=uid
        self.colour1=colour1
        self.colour2=colour2
        self.type=type
    def __repr__(self):
        return str(vars(self))

class Staff:
    def __init__(self,type,country,uid,BirthDate,First,Last,join_date):
        self.type=type
        self.country=country
        self.uid=uid
        self.BirthDate=BirthDate
        self.First=First
        self.Last=Last
        self.join_date=join_date
    def __repr__(self):
        return str(vars(self))

class Match:
    def __init__(self,id,away_team_id,away_team_name,competition_id,competition_name,game_date,home_team_id,home_team_name,matchday,period_1_start,period_2_start,season_id,season_name,Events):
        self.id=id
        self.away_team_id=away_team_id
        self.away_team_name=away_team_name
        self.competition_id=competition_id
        self.competition_name=competition_name
        self.game_date=game_date
        self.home_team_id=home_team_id
        self.home_team_name=home_team_name
        self.matchday=matchday
        self.period_1_start=period_1_start
        self.period_2_start=period_2_start
        self.season_id=season_id
        self.season_name=season_name
        self.Events=Events
    def __repr__(self):
        return str(vars(self))


class Event:
    def __init__(self,id,event_id,type_id,period_id,min,sec,player_id,team_id,outcome,x,y,timestamp,last_modified,version,Qs):
        self.id=id
        self.event_id=event_id
        self.type_id=type_id
        self.period_id=period_id
        self.min=min
        self.sec=sec
        self.player_id=player_id
        self.team_id=team_id
        self.outcome=outcome
        self.x=x
        self.y=y
        self.timestamp=timestamp
        self.last_modified=last_modified
        self.version=version
        self.Qs=Qs
    def __repr__(self):
        return str(vars(self))

class Qualifier:
    def __init__(self,id,qualifier_id,value):
        self.id=id
        self.qualifier_id=qualifier_id
        self.value=value
    def __repr__(self):
        return str(vars(self))

def ParseXmlToClassTeam(xmlfile):
    equipes=[]
    with open(xmlfile,'rb') as fd:
        doc = xmltodict.parse(fd.read())
        doc=doc['SoccerFeed']['SoccerDocument']
        for team in doc['Team']:

            Players=[]
            for joueur in team['Player']:
                uID=joueur['@uID']
                Name=joueur['Name']
                Position=joueur['Position']
                Stat={}
                for item in joueur['Stat']:
                    if '#text' in item:
                        Stat[item['@Type']]=item['#text']
                Players.append(Joueur(uID,Name,Position,Stat).__dict__)
            
            if isinstance(team['TeamKits']['Kit'],list):
                TeamKits=[]
                for kit in team['TeamKits']['Kit']:
                    id=kit['@id']
                    colour1=kit['@colour1']
                    if '@colour2' in kit:
                        colour2=kit['@colour2']
                    type=kit['@type']
                    TeamKits.append(KitEquipe(id,colour1,colour2,type).__dict__)

            else:
                id=team['TeamKits']['Kit']['@id']
                colour1=team['TeamKits']['Kit']['@colour1']
                colour2=team['TeamKits']['Kit']['@colour2']
                type=team['TeamKits']['Kit']['@type']
                TeamKits=KitEquipe(id,colour1,colour2,type).__dict__
            
            if isinstance(team['TeamOfficial'],list):
                TeamOfficals=[]
                for off in team['TeamOfficial']:
                    Type=off['@Type']
                    country = off['@country'] if '@country' in off else ''
                    uID=off['@uID']
                    BirthDate = off['PersonName']['BirthDate'] if 'BirthDate' in off['PersonName'] else ''
                    First=off['PersonName']['First']
                    Last=off['PersonName']['Last']
                    join_date=off['PersonName']['join_date']
                    TeamOfficals.append(Staff(Type,country,uID,BirthDate,First,Last,join_date).__dict__)
            else:
                Type=team['TeamOfficial']['PersonName']['@Type']
                country=team['TeamOfficial']['PersonName']['@country']
                uID=team['TeamOfficial']['PersonName']['@uID']
                BirthDate=team['TeamOfficial']['PersonName']['BirthDate']
                First=team['TeamOfficial']['PersonName']['First']
                Last=team['TeamOfficial']['PersonName']['Last']
                join_date=team['TeamOfficial']['PersonName']['join_date']
                TeamOfficals=Staff(Type,country,uID,BirthDate,First,Last,join_date).__dict__
            equipes.append(Equipe(team['@country'],team['@country_id'],team['@country_iso'],team['@region_id'],team['@region_name'],team['@short_club_name'],team['@uID'],team['@web_address'],team['Founded'],team['Name'],team['SYMID'],team['Stadium']['@uID'],team['Stadium']['Name'],team['Stadium']['Capacity'],TeamKits,Players,TeamOfficals).__dict__)
    return equipes


def ParseXMLToClassEvent(xml):
    with open(xml,'rb') as fd:
        doc=xmltodict.parse(fd.read())
        games=[]
        for g in doc['Games']['Game']:
            Events=[]
            for e in doc['Games']['Game']['Event']:
                Qs=[]
                if 'Q' in e:
                    if isinstance(e['Q'],list):
                        for q in e['Q']:
                            Qs.append(Qualifier(q['@id'],q['@qualifier_id'],q['@value'] if '@value' in q else '').__dict__)
                    else:
                        Qs=Qualifier(e['Q']['@id'],e['Q']['@qualifier_id'],e['Q']['@value'] if '@value' in e['Q'] else '').__dict__
                else:
                    Qs=''
                Events.append(Event(e['@id'],e['@event_id'],e['@type_id'],e['@period_id'],e['@min'],e['@sec'],e['@player_id'] if '@player_id' in e else '',e['@team_id'],e['@outcome'],e['@x'],e['@y'],e['@timestamp'],e['@last_modified'],e['@version'] if '@version' in e else '',Qs).__dict__)
            games.append(Match(doc['Games']['Game']['@id'],doc['Games']['Game']['@away_team_id'],doc['Games']['Game']['@away_team_name'],doc['Games']['Game']['@competition_id'],doc['Games']['Game']['@competition_name'],doc['Games']['Game']['@game_date'],doc['Games']['Game']['@home_team_id'],doc['Games']['Game']['@home_team_name'],doc['Games']['Game']['@matchday'],doc['Games']['Game']['@period_1_start'],doc['Games']['Game']['@period_2_start'],doc['Games']['Game']['@season_id'],doc['Games']['Game']['@season_name'],Events).__dict__)
    return games
start_time = time.time()
gameCollection = MongoClient('mongodb://localhost:27017/')['PSG']['games']
teamCollection = MongoClient('mongodb://localhost:27017/')['PSG']['teams']
equipes=ParseXmlToClassTeam('Noms des joueurs et IDs - F40 - L1 20162017.xml')
print("XML Teams+Joueurs Parsé en Classe Python --- %s seconds ---" % (time.time() - start_time))
for equipe in equipes:
    teamCollection.insert_one(equipe)
print("Classe Python Team+Joueurs inséré en BDD MongoDB --- %s seconds ---" % (time.time() - start_time))
for file in os.listdir("./data"):
    games=ParseXMLToClassEvent('./data/'+file)
    print("XML d'un Match Parsé en Classe Python --- %s seconds ---" % (time.time() - start_time))
    for game in games:
        gameCollection.insert_one(game)
    print("Classe Python d'un match inséré en base --- %s seconds ---" % (time.time() - start_time))
print("FIN --- %s seconds ---" % (time.time() - start_time))

