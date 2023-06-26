# Utilisation en local
La première fois après le `git clone` :
```
$ git submodule init
$ git submodule update
```

À chaque fois pour travailler en local :
```
$ hugo
$ hugo server -D
```

# Script pour créer un billet vide
```
DATE=2023-06-27 ./nouveau-billet.py "Co-pilote"
```

(après avoir fait `pip install -r requirements.txt` ou quelque chose de plus malin
genre pipenv)
