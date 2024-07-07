from gtts import gTTS
from pydub import AudioSegment
import sounddevice as sd
import numpy as np
import io

# Définir le texte à synthétiser
filename = "output.mp3"
texte = """Based on the data you provided, here is the weather forecast for Nantes, France. 
The current weather condition in Nantes is cloudy (broken clouds) with a temperature of 15.96 degrees Celsius (feels like 15.75 degrees Celsius). 
The minimum temperature for today is 15.96 degrees Celsius, while the maximum temperature can go up to 17.81 degrees Celsius. 
The humidity level is at 82% and the visibility is 10000 meters. 
The wind is coming from a west-southwest direction with a speed of 2.57 meters per second. 
The cloud coverage is 75% and is expected to stay cloudy for the rest of the day. 
The sun rises at 05:37 PM and sets at 12:24 AM, local time (DST). The timezone for Nantes is UTC +2. 
The weather data was last updated on Unix timestamp 1720215699, which corresponds to a specific date and time that will depend on the reference timezone. 
Overall, the weather in Nantes is cloudy and mild, with a comfortable temperature."""

tts = gTTS(text=texte, lang='en')
tts.save(filename)

# Enregistrez l'audio dans un objet BytesIO
mp3_fp = io.BytesIO()
tts.write_to_fp(mp3_fp)
mp3_fp.seek(0)

# Décodez les données MP3 en données audio brutes
audio = AudioSegment.from_mp3(mp3_fp)

# Convertissez les données audio en tableau NumPy
audio_data = np.array(audio.get_array_of_samples(), dtype=np.float32)

# Convertissez les données audio en format stéréo si nécessaire
if audio.channels == 2:
    audio_data = audio_data.reshape((-1, 2))

# Normalisez les données audio
audio_data = audio_data / np.max(np.abs(audio_data))

# Sélectionnez la sortie audio
print(sd.query_devices())
sd.default.device = 1
print(sd.query_devices())

# Jouez les données audio
sd.play(audio_data, audio.frame_rate)
sd.wait()  # Attend la fin de la lecture