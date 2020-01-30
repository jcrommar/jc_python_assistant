#import libraries

import speech_recognition as sr
import os
from gtts import gTTS
import datetime
import warnings
import calendar
import random
import wikipedia

#ignore warnings
warnings.filterwarnings('ignore')

#records the audio and returns a string
def recrodAudio():
    #create the audio recognizer, we are naming it r
    r = sr.Recognizer()
    #open mic and start recroding

    with sr.Microphone() as source:
        print('Say Something!')
        audio = r.listen(source)#records a single phrase

    #Speech recognition using Google's speech Recognition
    data = ''
    try: #try to get google to recognize the audio
        data = r.recognize_google(audio)
        print('You said: ' + data)
    except sr.UnknownValueError: #check for unknown errors
        print('Google Speech Recognition could not understand the audio, unknown error')
    except sr.RequestError as e: #check for request error
        print('Request results from Google Speech Recognition service error ' + e)

    return data

#Function to get a response from the assistant
def assistantResponse(text):
    print(text)

    #convert the text to speech
    myObj = gTTS(text=text, lang='en', slow=False)

    #save the audio to mp3 file
    myObj.save('assistant_response.mp3')

    #play the mp3 file
    os.system('start assistant_response.mp3')

#function to wake the assistant
def wakeCommand(text):
    WAKE_COMMANDS = ['hey Friday', 'okay Friday'] # list of wake up words/commands
    
    text = text.lower() #convert text to all lower case.
    # check users command/text contains a wake word
    for phrase in WAKE_COMMANDS:
        if phrase in text:
            return True
    
    #if the wake command wasn't found then return false
    return False
