from elevenlabs import play, save
from elevenlabs.client import ElevenLabs
import numpy as np
import matplotlib.pyplot as plt
import requests, os

client = ElevenLabs(
  api_key=os.environ["ELEVENLABS_1"], # Defaults to ELEVEN_API_KEY
)

try:
    audio = client.generate(
      text="""Hello world!""",
      voice="Sarah",
      model="eleven_multilingual_v2"
    )
    save(audio, "/home/bnj/RPi_prog/Morning_Brief/hello.mp3")
except Exception as e:
    print(f"Une erreur s'est produite : {e}")