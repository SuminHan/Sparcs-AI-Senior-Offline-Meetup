# Import necessary libraries
import requests  # Used for making HTTP requests
import json  # Used for working with JSON data
import time
import os
import utils

VOICE_ID_DICT = {
    'hero': '###'
    'again': '###'
}

def voice_test(text, singer):
    # Define constants for the script
    CHUNK_SIZE = 2048  # Size of chunks to read/write at a time
    XI_API_KEY = "###"  # Your API key for authentication
    VOICE_ID = VOICE_ID_DICT[singer]  # ID of the voice model to use
    TEXT_TO_SPEAK = text  # Text you want to convert to speech
    # print(text)
    sha256_hash = utils.hash_string(text, 'sha256')

    # Get the current time as a timestamp
    # current_time = time.time()
    OUTPUT_PATH = f"static/tmp/{sha256_hash}.mp3"  # Path to save the output audio file

    if os.path.isfile(OUTPUT_PATH):
        return {'url': f'/{OUTPUT_PATH}'}
    else:
        # Construct the URL for the Text-to-Speech API request
        tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream"

        # Set up headers for the API request, including the API key for authentication
        headers = {
            "Accept": "application/json",
            "xi-api-key": XI_API_KEY
        }

        # Set up the data payload for the API request, including the text and voice settings
        data = {
            "text": TEXT_TO_SPEAK,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.8,
                "style": 0.0,
                "use_speaker_boost": True
            }
        }


        # Make the POST request to the TTS API with headers and data, enabling streaming response
        response = requests.post(tts_url, headers=headers, json=data, stream=True)

        # Check if the request was successful
        if response.ok:
            # Open the output file in write-binary mode
            with open(OUTPUT_PATH, "wb") as f:
                # Read the response in chunks and write to the file
                for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    f.write(chunk)
            # Inform the user of success
            print("Audio stream saved successfully.")
        else:
            # Print the error message if the request was not successful
            print(response.text)

        return {'url': f'/{OUTPUT_PATH}'}


def hero_voice_test(text):
    return voice_test(text, 'hero')

def again_voice_test(text):
    return voice_test(text, 'again')
