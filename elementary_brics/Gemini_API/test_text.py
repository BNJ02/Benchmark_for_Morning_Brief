import google.generativeai as genai
import os

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

my_prompt = """
Tu es présentateur de la météo.
Ce texte sera utiliser ensuite pour une synthèse vocale, donc il faut qu'un synthétiseur vocal puisse lire clairement ton texte.
Aide toi du dictionnaire ci-dessous en utilisant tous les éléments pour réaliser ton bilan météo avec des commentaires sur les données. 
Exprime toi en parlant des prévisions de la journée qui arrive (nous sommes au tout début de la journée à 7 heures du matin) donc au temps du futur. 
Permet toi de donner des conseils ou des recommandations en fonction des données météo. 

Voici le dictionnaire avec les données météo sur différentes heures de la journée à utiliser:
{
      "dt": 1723453200,
      "main": {
        "temp": 26.41,
        "feels_like": 26.41,
        "temp_min": 26.41,
        "temp_max": 26.41,
        "pressure": 1010,
        "sea_level": 1010,
        "grnd_level": 1007,
        "humidity": 61,
        "temp_kf": 0
      },
      "weather": [
        {
          "id": 803,
          "main": "Clouds",
          "description": "broken clouds",
          "icon": "04d"
        }
      ],
      "clouds": { "all": 74 },
      "wind": { "speed": 3.88, "deg": 275, "gust": 4.83 },
      "visibility": 10000,
      "pop": 0,
      "sys": { "pod": "d" },
      "dt_txt": "2024-08-12 09:00:00"
    },
    {
      "dt": 1723464000,
      "main": {
        "temp": 31.56,
        "feels_like": 31.35,
        "temp_min": 31.56,
        "temp_max": 31.56,
        "pressure": 1010,
        "sea_level": 1010,
        "grnd_level": 1007,
        "humidity": 38,
        "temp_kf": 0
      },
      "weather": [
        {
          "id": 803,
          "main": "Clouds",
          "description": "broken clouds",
          "icon": "04d"
        }
      ],
      "clouds": { "all": 79 },
      "wind": { "speed": 4.41, "deg": 259, "gust": 4.2 },
      "visibility": 10000,
      "pop": 0,
      "sys": { "pod": "d" },
      "dt_txt": "2024-08-12 12:00:00"
    },
    {
      "dt": 1723474800,
      "main": {
        "temp": 27.9,
        "feels_like": 28.51,
        "temp_min": 27.9,
        "temp_max": 27.9,
        "pressure": 1010,
        "sea_level": 1010,
        "grnd_level": 1007,
        "humidity": 52,
        "temp_kf": 0
      },
      "weather": [
        {
          "id": 803,
          "main": "Clouds",
          "description": "broken clouds",
          "icon": "04d"
        }
      ],
      "clouds": { "all": 76 },
      "wind": { "speed": 6.82, "deg": 254, "gust": 6.19 },
      "visibility": 10000,
      "pop": 0,
      "sys": { "pod": "d" },
      "dt_txt": "2024-08-12 15:00:00"
    },
    {
      "dt": 1723485600,
      "main": {
        "temp": 22.75,
        "feels_like": 22.8,
        "temp_min": 22.75,
        "temp_max": 22.75,
        "pressure": 1011,
        "sea_level": 1011,
        "grnd_level": 1008,
        "humidity": 66,
        "temp_kf": 0
      },
      "weather": [
        {
          "id": 803,
          "main": "Clouds",
          "description": "broken clouds",
          "icon": "04d"
        }
      ],
      "clouds": { "all": 68 },
      "wind": { "speed": 7.32, "deg": 285, "gust": 10.01 },
      "visibility": 10000,
      "pop": 0,
      "sys": { "pod": "d" },
      "dt_txt": "2024-08-12 18:00:00"
    },
    {
      "dt": 1723496400,
      "main": {
        "temp": 17.19,
        "feels_like": 17.24,
        "temp_min": 17.19,
        "temp_max": 17.19,
        "pressure": 1012,
        "sea_level": 1012,
        "grnd_level": 1009,
        "humidity": 87,
        "temp_kf": 0
      },
      "weather": [
        {
          "id": 803,
          "main": "Clouds",
          "description": "broken clouds",
          "icon": "04n"
        }
      ],
      "clouds": { "all": 54 },
      "wind": { "speed": 3.83, "deg": 251, "gust": 6.06 },
      "visibility": 10000,
      "pop": 0,
      "sys": { "pod": "n" },
      "dt_txt": "2024-08-12 21:00:00"
    },
"""

model = genai.GenerativeModel("models/gemini-1.5-pro-latest")


### List of models that support generateContent ###
# print("List of models that support generateContent:\n")
# for m in genai.list_models():
#     if "generateContent" in m.supported_generation_methods:
#         print(m.name)

### Count Tokens
# Call `count_tokens` to get the input token count (`total_tokens`).
print("count_tokens: ", model.count_tokens(my_prompt))
response = model.generate_content(my_prompt)
print(response.usage_metadata)
# ( prompt_token_count: 11, candidates_token_count: 73, total_token_count: 84 )

### Génération de texte
response = model.generate_content(my_prompt)
print(response.text)


