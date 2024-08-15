import google.generativeai as genai
import os

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

myfile = genai.upload_file("/home/bnj/RPi_prog/Morning_Brief/elementary_brics/Gemini_API/MorningBrief.mp3")
print(f"{myfile=}")

model = genai.GenerativeModel("gemini-1.5-flash")
result = model.generate_content([myfile, "Describe this audio clip"])
print(result.text)