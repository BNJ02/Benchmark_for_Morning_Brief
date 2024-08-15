import requests, os, json

# Votre clé API OpenWeatherMap (inscrivez-vous sur https://openweathermap.org/api pour en obtenir une)
API_KEY = os.environ["OPEN_WEATHER_MAP_API_KEY"]

# La ville pour laquelle vous voulez récupérer la météo (par exemple, "Paris,fr")
VILLE = "Nantes,fr"

# L'unité de température (par exemple, "metric" pour le système métrique)
UNITE = "metric"

LIMIT = 5

lat=47.1667
lon=-1.5833

# L'URL de l'API OpenWeatherMap
URL = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units={UNITE}&appid={API_KEY}"
# http://api.openweathermap.org/data/2.5/weather?q={VILLE}&units={UNITE}&APPID={API_KEY}
# http://api.openweathermap.org/geo/1.0/direct?q={VILLE}&limit={LIMIT}&appid={API key}   &limit={LIMIT}

# Récupération des données météo
reponse = requests.get(URL)
donnees = reponse.json()

print(donnees)

# Écriture des données météo dans un fichier texte
with open("weather_overview.json", "w") as file:
    file.write(json.dumps(donnees))
