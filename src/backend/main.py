from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from google.cloud import texttospeech
import requests, os, json

from pydub import AudioSegment
import matplotlib.pyplot as plt
import numpy as np

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

################################################## WEATHER ##################################################

API_KEY = os.environ["OPEN_WEATHER_MAP_API_KEY"]
VILLE = "Nantes,fr"
UNITE = "metric"
LIMIT = 5
URL = f"http://api.openweathermap.org/data/2.5/weather?q={VILLE}&units={UNITE}&APPID={API_KEY}"

# Récupération des données météo
reponse = requests.get(URL)
weather_data = reponse.json()

filtered_weather_data = {
    "name": weather_data.get("name"),
    "weather": {
        "main": weather_data.get("weather")[0].get("main"),
        "description": weather_data.get("weather")[0].get("description")
    },
    "main": {
        "temp": weather_data["main"].get("temp"),
        "feels_like": weather_data["main"].get("feels_like"),
        "temp_min": weather_data["main"].get("temp_min"),
        "temp_max": weather_data["main"].get("temp_max"),
        "pressure": weather_data["main"].get("pressure"),
        "humidity": weather_data["main"].get("humidity")
    }
}

################################################## NEWS ##################################################

API_KEY = os.environ["NEWS_API_KEY"]
PAYS = "fr"
URL = f"https://newsapi.org/v2/top-headlines?country={PAYS}&apiKey={API_KEY}"

reponse = requests.get(URL)
donnees = reponse.json()

# Création de la liste des titres et auteurs
titres_et_auteurs = []
for article in donnees["articles"]:
    titre = article["title"]
    auteur = article.get("author", "Auteur inconnu")  # Utilisation d'une valeur par défaut si l'auteur est manquant
    titres_et_auteurs.append([titre, auteur])

################################################## AI ##################################################
api_key = os.environ["MISTRAL_API_KEY"]

##### WEATHER #####
content = """
Ce texte sera utiliser ensuite pour une synthèse vocale. 
A partir de ce format dictionnaire, utilise tous les éléments 
pour réaliser un bilan météo concis avec des commentaires sur 
les données (par exemple : une température ou une humidité 
anormalement élevé pour la période), sachant que l'élément 
"feels_like" est la température ressentie et que la pression 
est exprimée en hectoPascal. Ne cite pas de noms d'éléments. 
Arrondie les températures à la décimale. Ecris les unités en 
toutes lettres. Exprime toi en parlant des prévisions de la 
journée qui arrive (nous sommes au tout début de la journée 
à 6 heures) donc au temps du futur. Permets toi de donner 
des conseils ou des recommandations en fonction des données météo. 
""" + json.dumps(filtered_weather_data)

# Params IA
model = "mistral-large-latest"
client = MistralClient(api_key=api_key)
messages = [
    ChatMessage(role="user", content=content)
]

# No streaming
chat_response = client.chat(
    model=model,
    messages=messages,
)

weather_review = chat_response.choices[0].message.content

##### NEWS #####
thematics_list = ['sport', 'culture', 'technologie', 'santé', 'politique', 'économie', 'environnement', 'faits divers', 'international', 'société']
content = """
Ce texte sera utiliser ensuite pour une synthèse vocale.
A partir de cette liste, utilise tous les éléments pour réaliser un point info quotidien sur l'actualité de manière concise.
Regroupe les différents titres par thématique en annonçant la thématique avant de donner les titres, ne reviens pas sur une thématique déjà abordée.
Fais des transitions entre les différents titres.
Ne fais pas de point par thématique !
""" + str(titres_et_auteurs)

messages = [
    ChatMessage(role="user", content=content)
]

# No streaming
chat_response = client.chat(
    model=model,
    messages=messages,
)
news_review = chat_response.choices[0].message.content

################################################## TTS ##################################################
# Texte complet
complete_text = weather_review + "\n\n\nMaintenant, nous allons passer aux actualités !\n\n\n" + news_review

with open("MorningBrief.txt", "w") as fichier:
    fichier.write(complete_text)

output_file = "MorningBrief.mp3"
text_to_speech(complete_text, output_file)

################################################## Analyse ##################################################

mp3_fp = 'MorningBrief.mp3'
audio = AudioSegment.from_mp3(mp3_fp)

# Convertir les données audio en tableau NumPy
audio_data = np.array(audio.get_array_of_samples(), dtype=np.float32)

# Normaliser les données audio
audio_data_normalized = audio_data / np.max(np.abs(audio_data))

# Visualisation des données audio
plt.figure()  # Crée une nouvelle figure pour le tracé temporel
time = np.arange(len(audio_data)) / audio.frame_rate
plt.plot(time, audio_data)
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('Audio Data')
plt.savefig('MorningBrief_waveform.png')


# Visualisation du spectrogramme
plt.figure()  # Crée une nouvelle figure pour le spectrogramme
if audio_data.ndim == 2:
    Pxx, freqs, bins, im = plt.specgram(audio_data[:, 0], Fs=audio.frame_rate)
else:
    Pxx, freqs, bins, im = plt.specgram(audio_data, Fs=audio.frame_rate)
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
plt.title('Spectrogram')
plt.colorbar(im).set_label('Intensity (dB)')
plt.savefig('MorningBrief_spectrogram.png')


# Visualisation du spectre
plt.figure()  # Crée une nouvelle figure pour le spectre

# Calculer la transformée de Fourier du signal audio
n = len(audio_data)
k = np.arange(n) # Crée un tableau de fréquences
T = n / audio.frame_rate # Durée de l'enregistrement audio
frq = k / T # De 0 à la fréquence de Nyquist
freq = frq[range(int(n/2))] # Moitié du spectre de fréquence (unilatéral)

# Calculer l'amplitude du spectre
audio_fft = np.fft.fft(audio_data)
audio_fft = audio_fft / n
audio_spectrum = 2 * np.abs(audio_fft[0:int(n/2)])

# Tracer le spectre
amplitude_dB = 20 * np.log10(audio_spectrum)
plt.plot(freq, amplitude_dB)
plt.xlabel('Fréquence (Hz)')
plt.ylabel('Amplitude (dB)')
plt.title('Spectre du signal audio')
plt.savefig('MorningBrief_spectre.png')