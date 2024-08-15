from GoogleNews import GoogleNews
import google.generativeai as genai
from google.cloud import texttospeech
import os
import json

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def text_to_speech(text, output_file):
    # Instanciez le client Text to Speech
    client = texttospeech.TextToSpeechClient()

    # AU, GB, US, IN pour l'anglais : en
    # FR, CA pour le français : fr

    # Définissez les paramètres de la voix
    voice = texttospeech.VoiceSelectionParams(
        name='fr-FR-Wavenet-C',
        language_code="fr-FR"
        # ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Définissez les paramètres de l'audio
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=1.15
    )

    # Créez la requête de synthèse vocale
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Créez la requête de synthèse vocale
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    # Enregistrez l'audio dans un fichier
    with open(output_file, "wb") as out:
        out.write(response.audio_content)


#################### NEWS PART ####################
googlenews = GoogleNews()

googlenews.set_lang('fr')
googlenews.set_period('1d')
googlenews.set_encode('utf-8')
# googlenews.set_time_range('08/11/2024','08/11/2024')

# Theme du brief
googlenews.get_news('Sciences et Technologies')

result = googlenews.results()
print("Total news : ",len(result))

# Liste de tous les titres
titles = [x['title'] for x in result]
print("Titles:", titles)

# Écriture des données météo dans un fichier texte
with open("theme_brief_w_AI.json", "w") as file:
    file.write(json.dumps(result))

googlenews.clear()

#################### AI PART ####################
model = genai.GenerativeModel("models/gemini-1.5-pro-latest")

my_prompt = """
Tu es présentateur des actualités.
Fais une synthèse des sujets les plus récurrents dans les actualités du jour.
Evoque au maximum 5 sujets différents.
Réalise qu'un seul paragraphe mais avec une introduction et un mot d'au revoir.
""" + "\n".join(titles)

### Count Tokens
# Call `count_tokens` to get the input token count (`total_tokens`).
print("count_tokens: ", model.count_tokens(my_prompt))
response = model.generate_content(my_prompt)
print(response.usage_metadata)

### Génération de texte
response = model.generate_content(my_prompt)
print(response.text)

### Text to Speech
output_file = "SportBrief.mp3"
text_to_speech(response.text, output_file)