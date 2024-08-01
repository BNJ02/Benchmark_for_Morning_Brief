from google.cloud import texttospeech

client = texttospeech.TextToSpeechClient()

voices = client.list_voices()

# Créer une liste pour stocker les noms de voix
english_voice_names = []
french_voice_names = []

print("-" * 20)
for voice in voices.voices:
    if "en-US" in voice.name: #"Standard" in voice.name and 
        print(f"Voice Name: {voice.name}")
        print(f"Gender: {voice.ssml_gender}")
        print("-" * 20)
        english_voice_names.append(voice.name)
    if "Standard" in voice.name and "fr" in voice.name:
        french_voice_names.append(voice.name)

print(english_voice_names)
print(french_voice_names)
