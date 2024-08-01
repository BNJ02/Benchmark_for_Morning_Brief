import requests, os, json

# Votre clé API NewsAPI (inscrivez-vous sur https://newsapi.org/ pour en obtenir une)
API_KEY = os.environ["NEWS_API_KEY"]

# Le pays pour lequel vous voulez récupérer les actualités (par exemple, "fr" pour la France)
PAYS = "fr"

# L'URL de l'API NewsAPI
URL = f"https://newsapi.org/v2/top-headlines?country={PAYS}&apiKey={API_KEY}"

# Récupération des données d'actualités
reponse = requests.get(URL)
donnees = reponse.json()

print(donnees)

# Écriture des données météo dans un fichier texte
with open("news.json", "w") as fichier:
    fichier.write(json.dumps(donnees))

# Écriture des titres et des résumés des actualités dans un fichier texte
with open("news.txt", "w") as fichier:
    for article in donnees["articles"]:
        titre = article["title"]
        resume = article["description"]
        fichier.write(f"{titre}\n{resume}\n---\n")
