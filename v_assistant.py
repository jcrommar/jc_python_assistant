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
def recordAudio():
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

#function to get date
def getDate():
    now = datetime.datetime.now()
    my_date = datetime.datetime.today()
    weekday = calendar.day_name[my_date.weekday()]
    monthNum = now.month
    dayNum = now.day

    month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
                   'October', 'November', 'December']
    ordinalNumbers = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th',
                      '13th', '14th', '15th', '16th', '17th', '18th', '19th', '20th', '21st', '22nd', '23rd',
                      '24th', '25th', '26th', '27th', '28th', '29th', '30th', '31st']
    return 'Today is' + weekday + ' ' + month_names[monthNum - 1] + ' the ' + ordinalNumbers[dayNum - 1] + '.'

#function to return a random greeting response
def greeting(text):
    #greeting inputs
    GREETING_INPUTS = ['hi, Friday', 'hey, Friday', 'hola, Friday', 'greetings, Friday', 'yes, Friday', 'hello, Friday']

    #greetins back to JC
    GREETING_RESPONSES = ['howdy', 'hello', 'hey there', 'yes sir']

    #if the user input is a greeting, then return a randomly chosen greeting respone
    for word in text.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES) + '.'

    #if no greeting was detected then return an empty string
    return ''

#function to get person's firts name and last name
def getPerson(text):
    wordList = text.split() # split text into list of words

    for i in range(0, len(wordList)):
        if i + 3 <= len(wordList) - 1 and wordList[i].lower() == 'who' and wordList[i + 1].lower() == 'is':
            return wordList[i + 2] + ' ' + wordList[i + 3]

while True:
    #record the audio
    text = recordAudio()
    response = '' #empty response to append the text

    #checking the wake word/phrase
    if (wakeCommand(text) == True):

        #check for greetings by the user
        response = response + greeting(text)

        #check for user request with date information
        if ('date' in text):
            get_date = getDate()
            response = response + ' ' + get_date

        #check for user request with time information
        if ('time' in text):
            now = datetime.datetime.now()
            meridiem = ''
            if now.hour >= 12:
                meridiem = 'p.m'
                hour = now.hour - 12
            else:
                meridiem = 'a.m'
                hour = now.hour

            #convert minute into proper string
            if now.minute < 10:
                minute = '0'+str(now.minute)
            else:
                minute = str(now.minute)

            response = response + ' '+ 'It is '+ str(hour)+ ':'+minute+' '+meridiem+' .'

        #check to see if the user said 'who is'
        if ('who is' in text):
            person = getPerson(text)
            wiki = wikipedia.summary(person, sentences=2)
            response = response + ' ' + wiki
        
        #have Friday response back using audio and the text from the response
        assistantResponse(response)