import whisper

model = whisper.load_model("base")
result = model.transcribe("ElevenLabs_Chris_TTS_Neural_Network.mp3")
print(result["text"])