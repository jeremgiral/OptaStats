#install.packages('mongolite')
library(mongolite)
dataEvents <- mongo(collection = "games", db = "PSG", url = "mongodb://localhost:27017")
dataTeams <- mongo(collection = "teams", db = "PSG", url = "mongodb://localhost:27017")
dataSample <- mongo(collection = "sample", db = "PSG", url = "mongodb://localhost:27017")
dataEvents$find(limit = 1)$Events[[1]]$Qs

#install.packages("RPostgreSQL")
require("RPostgreSQL")
drv <- dbDriver("PostgreSQL")
con <- dbConnect(drv, dbname = "postgres",
                 host = "localhost", port = 5432,
                 user = "postgres", password = "jeremy")


# Attention R écrit beaucoup en mémoire, ça risque de faire planté le pc de faire ce select sans filtre (where) ! 
# Ca te permet d'avoir le modèle de données !
events <- dbGetQuery(con, "select dq.nom qualifier,dq.description,dq.valeur,q.valeur,e.event_id,de.nom evenement,de.description,e.type_id,e.period_id,e.minuts,e.sec,e.idteam,e.outcome,e.x,e.y,e.t_timestamp,home_team_name,away_team_name,competition_name,game_date, period_1_start, period_2_start, eq.nom equipe_joueur,j1.nom joueur,j1.poste,j1.real_position,j1.real_position_side
from qualifier q
inner join events e on q.idevent=e.idevent
inner join matchs m on e.idmatch=m.idmatch
inner join equipe eq on eq.idequipe=e.idteam
inner join dimqualifier dq on q.qualifier_id=dq.idqualifier
left join joueur j1 on j1.idjoueur=e.idplayer
left join dimevent de on de.eventid=e.event_id
limit 1000")
events