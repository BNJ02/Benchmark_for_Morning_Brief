from pydub import AudioSegment
import sounddevice as sd
import numpy as np

# Charger le fichier MP3
filename = "MorningBrief.mp3"
audio = AudioSegment.from_mp3(filename)

# Convertir les données audio en tableau NumPy
audio_data = np.array(audio.get_array_of_samples(), dtype=np.float32)

# Convertir les données audio en format stéréo si nécessaire
if audio.channels == 2:
    audio_data = audio_data.reshape((-1, 2))

# Normaliser les données audio
audio_data_normalized = audio_data / np.max(np.abs(audio_data))

# Sélectionner la sortie audio
print(sd.query_devices())
sd.default.device = 1  # Remplacez par l'index de votre périphérique audio
print(sd.query_devices())

# Jouer les données audio
sd.play(audio_data_normalized, audio.frame_rate)
sd.wait()  # Attend la fin de la lecture