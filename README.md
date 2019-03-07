#### Pour construire la database :

- 1 - Installer Docker

- 2 - Dans une invite de commande se placer à la racine du projet

- 3 - Exécuter la commande suivante : 
```
docker build -t=mongodb . && docker run -p 27017:27017 mongodb
```

- 4 - Dans une autre invite de commande (à la racine du projet) : 
```
python main_psgx.py
```

- 5 - Pour utiliser la BDD dans R :
```
library(mongolite)
dataEvents = mongo(collection = "games", db = "PSG", url = "mongodb://localhost:27017")
dataTeams  = mongo(collection = "teams", db = "PSG", url = "mongodb://localhost:27017")
```