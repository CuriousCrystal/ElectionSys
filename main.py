
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
    base_url="https://api.x.ai/v1"
)


import requests
import json

# Define the Event Coordination Tools for OpenAI
event_tools = [
    {
        "type": "function",
        "function": {
            "name": "get_wait_times",
            "description": "Get the current real-time crowd density and wait times for all areas in the event venue.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_best_route",
            "description": "Ask the system for the best, least crowded gate and restroom automatically.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]

def fetch_events_api(endpoint):
    try:
        res = requests.get(f"http://localhost:8000/api/{endpoint}")
        return json.dumps(res.json())
    except:
        return json.dumps({"error": "Event server offline."})

def ai(query):
    # Keep standard completion for long-form essays
    text = f"AI Response for Prompt: {query}\n *********************************************\n\n\n\n"
    try:
        # Call the OpenAI API to get the response
        response = client.chat.completions.create(
            model="grok-beta",
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


chat_history = [
    {"role": "system", "content": "You are August, the official Event Concierge Assistant. You help attendees navigate the physical event, manage crowds, find restrooms, and fetch real-time wait times. Be warm and efficient. Always use your available tools to check wait times before recommending a route!"}
]

def chat(query):
    chat_history.append({"role": "user", "content": query})
    try:
        response = client.chat.completions.create(
            model="grok-beta",
            messages=chat_history,
            tools=event_tools,
            temperature=0.7
        )
        
        message = response.choices[0].message
        
        # Check if the AI wants to use a tool to fetch live data
        if message.tool_calls:
            chat_history.append(message) # Append the assistant's request to use a tool
            
            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                if function_name == "get_wait_times":
                    result = fetch_events_api("zones")
                elif function_name == "get_best_route":
                    result = fetch_events_api("recommendations")
                else:
                    result = "{}"
                    
                chat_history.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })
                
            # Second call to get the synthesized response based on the new data
            second_response = client.chat.completions.create(
                model="grok-beta",
                messages=chat_history,
                temperature=0.7
            )
            final_response = second_response.choices[0].message.content
            chat_history.append({"role": "assistant", "content": final_response})
            print(f"August: {final_response}")
            speak(final_response)
            return final_response
            
        else:
            final_response = message.content
            chat_history.append({"role": "assistant", "content": final_response})
            print(f"August: {final_response}")
            speak(final_response)
            return final_response
            
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
                return input("Please type your command: ")

            try:
                print("Recognizing...")
                text = ans.recognize_google(audio, language="en-in")
                print(f"You said: {text}")
                return text
            except sr.UnknownValueError:
                print("Sorry, could not understand the audio.")
                return input("Please type your command: ")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
                return input("Please type your command: ")
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
    
    # If the user just pressed Enter without typing anything, don't do anything
    if not query.strip():
        continue

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
