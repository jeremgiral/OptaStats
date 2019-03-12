#### Pour construire la database MongoDB(NoSQL) :

- 1 - Installer Docker

- 2 - Dans une invite de commande se placer dans ./init-data/NoSQL

- 3 - Exécuter la commande suivante : 
```
docker build -t=mongodb . && docker run -d -p 27017:27017 mongodb
```

- Ne pas oublier de télécharger les fichiers XML sources et de les dézipper dans un dossier nommé *'/data'*

- 4 - Dans une autre invite de commande : 
```
python main_psgx.py
```

- 5 - Pour utiliser la BDD dans R :
```
library(mongolite)
dataEvents <- mongo(collection = "games", db = "PSG", url = "mongodb://localhost:27017")
dataTeams <- mongo(collection = "teams", db = "PSG", url = "mongodb://localhost:27017")
dataSample <- mongo(collection = "sample", db = "PSG", url = "mongodb://localhost:27017")
dataEvents$find(limit = 1)$Events[[1]]$Qs
```

#### Pour construire la database MongoDB(NoSQL) :

- 1 : Installer Docker

- 2 - Dans une invite de commande se placer dans ./init-data/SQL

- 3 - Exécuter les commande suivante : 

```
docker run --rm  --name pg-docker -e POSTGRES_PASSWORD=jeremy -d -p 5432:5432 postgres
```
```
docker cp backup.dump pg-docker:/var/lib/postgresql/data/backup.dump
```
```
docker exec pg-docker sh -c "pg_restore -U postgres -d postgres -v /var/lib/postgresql/data/backup.dump"
```


