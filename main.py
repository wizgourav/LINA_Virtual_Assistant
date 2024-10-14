import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI 
from gtts import gTTS
import pygame
import os

recognizer = sr.Recognizer() #When we will speak the recognizer object recognizes it
engine = pyttsx3.init() #Intializes pyttsx


def speak(text):
    voices = engine.getProperty('voices')

# Change to a specific voice (e.g., female voice)
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()

# def speak(text):
#     tts = gTTS(text)
#     tts.save('temp.mp3')
#         # Initialize pygame
#     pygame.mixer.init()

#     # Load the MP3 file
#     pygame.mixer.music.load("temp.mp3")

#     # Play the file
#     pygame.mixer.music.play()

#     # Keep the program running while the music plays
#     while pygame.mixer.music.get_busy():
#         pygame.time.Clock().tick(10)
    
#     pygame.mixer.music.unload()
#     os.remove("temp.mp3") 


def aiProcess(command):   
    client = OpenAI(
        api_key="YOUR API KEY"
    )

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a Virtual assistant named Jarvis skilled in general tasks like Alexa and Google. Give Short responses. "},
            { "role": "user","content": command }
        ]
    )

    return completion.choices[0].message.content

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com") 
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com") 
    elif "open gmail" in c.lower():
        webbrowser.open("https://gmail.com") 
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link) 
    elif "news" in c.lower():
        r = requests.get("Your Api Key")
        if r.status_code == 200:
            #Parse the JSON Response
            data = r.json()
            #Extract the articles
            articles = data.get('articles' , [])
            #Print the articles
            for article in articles:
                speak(article['title'])
    
    else:
        #Let openAI handle the request
        output = aiProcess(c)
        speak(output)

if __name__ == "__main__" :
    speak("Initializing Lina....")
    speak("Hello Sir...If you need any help just call my name")
    while True:
    #Listen for the wake word Jarvis
        r  = sr.Recognizer()
        print("Recognizing.....")
        try:
            with sr.Microphone() as source :
                print("Listening....")
                audio = r.listen(source , timeout=2 , phrase_time_limit=1)
            word = r.recognize_google(audio)
            if(word.lower() == "lina"):
                speak("Yaa")
                #Listen for command
                with sr.Microphone() as source :
                    print("Lina Activated....")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)

        except Exception as e:
            print("Error;{0}".format(e))