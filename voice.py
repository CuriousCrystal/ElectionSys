import gtts
import playsound
import win32com.client

import os

def gttsSpeak(query):
    test = query
    sound = gtts.gTTS(test, lang="hi")
    sound.save("temp_voice.mp3")
    playsound.playsound("temp_voice.mp3")
    os.remove("temp_voice.mp3")


def winSpeak(query, voice_id=1):
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    # Get all available voices
    voices = speaker.GetVoices()
    # Set the voice (0 for David/Male, 1 for Zira/Female)
    try:
        speaker.Voice = voices.Item(voice_id)
    except Exception as e:
        print(f"Warning: Could not change voice: {e}")
    speaker.Speak(query)

# winSpeak("aisha")



# from vosk import Model,KaldiRecognizer
# import pyaudio
#
# model = Model("./vosk/vosk-model-small-en-in-0.4")
# recognizer = KaldiRecognizer(model, 16000)
#
# mic = pyaudio.PyAudio()
# stream = mic.open(rate=1600, channels=1, format=pyaudio.paInt16, input=True,
#                   frames_per_buffer=8192)
# stream.start_stream()
# while True:
#     data = stream.read(4096)
#     if recognizer.AcceptWaveform(data):
#         print(recognizer.Result())
