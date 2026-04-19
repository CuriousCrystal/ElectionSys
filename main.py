
import speech_recognition as sr
import webbrowser
import os
import datetime
from openai import OpenAI
from config import apikey
from voice import winSpeak
import sys

# Initialize OpenAI client
client = OpenAI(
    api_key=apikey,
    base_url="https://openrouter.ai/api/v1"
)


# Initialize chatStr variable
chatStr = ""

# Function to generate chat-based response using Grok API
def ai(query):
    # Create the text variable to store the response
    text = f"AI Response for Prompt: {query}\n *********************************************\n\n\n\n"

    try:
        # Call the OpenAI API to get the response
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are August, a friendly and helpful AI assistant. Speak in a casual, warm, and conversational tone. Use simple language and be enthusiastic about helping."
                },
                {
                    "role": "user",
                    "content": query
                }
            ],
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        # Extract response text
        if response.choices and len(response.choices) > 0:
            response_text = response.choices[0].message.content
            text += response_text

        # Create the "Responses" directory if it doesn't exist
            if not os.path.exists("Responses"):
                os.mkdir("Responses")

            # Save the response text to a file
            with open(f"Responses/{''.join(query.split('intelligence')[1:]).strip()}.txt", "w") as f:
                f.write(text)
            print(text)
        else:
            print("Error: No response from API.")
    except Exception as e:
        print(f"Error calling AI: {e}")


def chat(query):
    global chatStr

    chatStr += f"User: {query}\nAugust: "
    
    try:
        # Call the OpenAI API to get the response
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are August, a friendly and helpful AI assistant. Speak in a casual, warm, and conversational tone. Use simple language and be enthusiastic about helping."
                },
                {
                    "role": "user",
                    "content": chatStr
                }
            ],
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        # Extract response text
        if response.choices and len(response.choices) > 0:
            response_text = response.choices[0].message.content
            chatStr += f"{response_text}\n"
            print(chatStr)
            speak(response_text)
            return response_text
        else:
            print("Error: No response from API.")
            return ""
    except Exception as e:
        print(f"Error in chat: {e}")
        return ""


def takeCommand():
    """Take command from microphone with fallback to text input"""
    try:
        ans = sr.Recognizer()
        with sr.Microphone() as source:
            print('Listening...')
            ans.pause_threshold = 1
            ans.energy_threshold = 300
            try:
                ans.adjust_for_ambient_noise(source, duration=0.5)
            except:
                pass
            
            try:
                audio = ans.listen(source, timeout=5, phrase_time_limit=10)
            except sr.WaitTimeoutError:
                print("Listening timed out.")
                return ""

            try:
                print("Recognizing...")
                text = ans.recognize_google(audio, language="en-in")
                print(f"You said: {text}")
                return text
            except sr.UnknownValueError:
                print("Sorry, could not understand the audio.")
                return ""
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
                return ""
    except Exception as e:
        print(f"Microphone not available: {e}")
        print("Falling back to text input...")
        text = input("Enter your command: ")
        return text

def speak(query):
    winSpeak(query)

query = "Hey, I'm August."
speak(query)
while True:
    query = takeCommand()
    # todo Add more sites
    sites = [["youtube", "https://www.youtube.com/"], ["instagram", "https://www.instagram.com/"],
             ["facebook", "https://www.facebook.com/"],
             ["wikipedia", "https://www.wikipedia.org/"], ["google", "https://www.google.com/"]]

    for site in sites:
        if f"Open {site[0]}".lower() in query.lower():
            query = f"Opening {site[0]} sir..."
            webbrowser.open(site[1])
            speak(query)

    if "open music" in query:
        musicPath = "https://music.youtube.com/"
        query = f"Opening music"
        speak(query)
        webbrowser.open(musicPath)

    elif "Using artificial intelligence".lower() in query.lower():
        ai(query)

    elif "input query".lower() in query.lower():
        query = input("Enter any query: ")
        speak(f"Your query is {query}")
        ai(query)

    elif "the time" in query:
        hour = datetime.datetime.now().strftime("%H")
        min = datetime.datetime.now().strftime("%M")
        sec = datetime.datetime.now().strftime("%S")
        speak(f"Sir Time is {hour} bus ke {min} minutes or {sec} second")

    elif any(word in query.lower() for word in ["august quit", "exit", "goodbye", "bye", "see you", "farewell", "stop"]):
        speak(f"Goodbye! Have a great day.")
        exit()

    else:
        chat(query)
