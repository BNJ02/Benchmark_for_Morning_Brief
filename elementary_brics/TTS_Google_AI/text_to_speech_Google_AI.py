from google.cloud import texttospeech

def text_to_speech(text, output_file):
    # Instanciez le client Text to Speech
    client = texttospeech.TextToSpeechClient()

    # AU, GB, US, IN pour l'anglais : en
    # FR, CA pour le français : fr

    # Définissez les paramètres de la voix
    voice = texttospeech.VoiceSelectionParams(
        name='en-US-Wavenet-J',
        language_code="en-US"
        # ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Définissez les paramètres de l'audio
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
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

if __name__ == "__main__":
    text = """
Neural networks are one of the most beautiful programming paradigms ever invented. 
In the conventional approach to programming, we tell the computer what to do, breaking big problems up into many small, precisely defined tasks that the computer can easily perform. 
By contrast, in a neural network we don't tell the computer how to solve our problem. 
Instead, it learns from observational data, figuring out its own solution to the problem at hand.

Automatically learning from data sounds promising. 
However, until 2006 we didn't know how to train neural networks to surpass more traditional approaches, except for a few specialized problems. 
What changed in 2006 was the discovery of techniques for learning in so-called deep neural networks. 
These techniques are now known as deep learning.
They've been developed further, and today deep neural networks and deep learning achieve outstanding performance on many important problems in computer vision, speech recognition, and natural language processing. 
They're being deployed on a large scale by companies such as Google, Microsoft, and Facebook.

The purpose of this book is to help you master the core concepts of neural networks, including modern techniques for deep learning.
After working through the book you will have written code that uses neural networks and deep learning to solve complex pattern recognition problems.
And you will have a foundation to use neural networks and deep learning to attack problems of your own devising.
    """
    output_file = "output.mp3"
    text_to_speech(text, output_file)
