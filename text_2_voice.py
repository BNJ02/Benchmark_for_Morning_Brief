from gtts import gTTS
from pydub import AudioSegment
import sounddevice as sd
import numpy as np
import io
import matplotlib.pyplot as plt

# Définir le texte à synthétiser
filename = "output.mp3"
texte = """Based on the data you provided, here is the weather forecast for Nantes, France."""

tts = gTTS(text=texte, lang='en', tld='co.uk')
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
audio_data_normalized = audio_data / np.max(np.abs(audio_data))

# Sélectionnez la sortie audio
print(sd.query_devices())
sd.default.device = 1
print(sd.query_devices())

# Jouez les données audio
sd.play(audio_data_normalized, audio.frame_rate)
sd.wait()  # Attend la fin de la lecture



# Visualisation des données audio
plt.figure()  # Crée une nouvelle figure pour le tracé temporel
time = np.arange(len(audio_data)) / audio.frame_rate
plt.plot(time, audio_data)
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('Audio Data')
plt.savefig('waveform.png')


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
plt.savefig('spectrogram.png')


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
plt.savefig('spectre.png')