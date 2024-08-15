import requests
import json

url = 'http://localhost:11434/api/generate'
data = {
    "model": "gemma2:2b",
    "prompt": """
Ce texte sera utiliser ensuite pour une synthèse vocale. Soit bavard ! Ait un langage entre soutenu et familier !
A partir de ce format dictionnaire, utilise tous les éléments pour réaliser un bilan météo 
avec des commentaires sur les données (par exemple : une température ou une humidité 
anormalement élevé pour la période), sachant que la pression est exprimée en hectoPascal. 
Ecris les unités en toutes lettres ainsi que le pourcentage pour l'humidité (°C devient degré, 
° devient degré, % devient pourcentage). Arrondie les températures à la décimale.Exprime toi en parlant 
des prévisions de la journée qui arrive (nous sommes au tout début de la journée à 7 heures 
du matin) donc au temps du futur. Permets toi de donner des conseils ou des recommandations 
en fonction des données météo.

Voici le dictionnaires avec les données :
{
    "coord": {
        "lon": -1.5833,
        "lat": 47.1667
    },
    "weather": [
        {
            "id": 800,
            "main": "Clear",
            "description": "clear sky",
            "icon": "01d"
        }
    ],
    "base": "stations",
    "main": {
        "temp": 32.17,
        "feels_like": 34.2,
        "temp_min": 27.81,
        "temp_max": 32.78,
        "pressure": 1011,
        "humidity": 48,
        "sea_level": 1011,
        "grnd_level": 1008
    },
    "visibility": 10000,
    "wind": {
        "speed": 3.09,
        "deg": 250
    },
    "clouds": {
        "all": 0
    },
    "dt": 1722441879,
    "sys": {
        "type": 1,
        "id": 6574,
        "country": "FR",
        "sunrise": 1722401054,
        "sunset": 1722454861
    },
    "timezone": 7200,
    "id": 2990968,
    "name": "Arrondissement de Nantes",
    "cod": 200
}
"""
}

headers = {
    'Content-Type': 'application/json'
}

response = requests.post(url, data=json.dumps(data), headers=headers)

# Initialiser une liste pour stocker les valeurs de 'response'
response_values = []

# Essayer de décoder la réponse en JSON
try:
    # Si la réponse contient plusieurs objets JSON, les séparer et les traiter individuellement
    responses = response.text.split('\n')
    for resp in responses:
        if resp.strip():  # Ignorer les lignes vides
            response_json = json.loads(resp)
            response_values.append(response_json['response'])
except json.JSONDecodeError as e:
    print("Erreur de décodage JSON :", e)

# Concaténer les valeurs de 'response' en un seul texte
final_text = ''.join(response_values)

# Afficher le texte final
print(final_text)

# Sauvegarder le texte final dans un fichier texte
with open('response_output.txt', 'w') as file:
    file.write(final_text)