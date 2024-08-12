import speech_recognition as sr
import datetime
import subprocess
import pywhatkit
import pyttsx3
import wikipedia
import webbrowser

from voiceassistant import speak


# Initialize Text-to-Speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Set voice (consider adding a choice for the user)

# Create a recognizer instance
recognizer = sr.Recognizer()


def listen_and_respond():
    """Listens for user input and responds accordingly"""
    with sr.Microphone() as source:
        print("Clearing background noises... Please wait")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print('Ask me anything..')
        recorded_audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(recorded_audio, language='en-US')
        text = text.lower()
        print('Your message:', text)

        handle_command(text)  # Delegate task handling to dedicated function

    except Exception as ex:
        print(f"An error occurred: {ex}")
        engine.say("Sorry, I didn't understand that.")
        engine.runAndWait()


def handle_command(text):
    """Handles different user commands based on keywords"""
    if 'chrome' in text:
        open_chrome()
    elif 'time' in text:
        tell_time()
    elif 'play' in text or 'youtube' in text:
        play_video(text)
    elif 'wikipedia' in text:
        search_wikipedia(text)  # Added wikipedia search functionality


def open_chrome():
    """Opens Chrome browser"""
    program_name = "C:\Program Files\Google\Chrome\Application\chrome.exe"
    try:
        subprocess.Popen([program_name])
        engine.say("Opening Chrome.")
        engine.runAndWait()
    except Exception as ex:
        print(f"Error opening Chrome: {ex}")
        engine.say("Sorry, there might be a problem opening Chrome.")
        engine.runAndWait()


def tell_time():
    """Retrieves and announces the current time"""
    current_time = datetime.datetime.now().strftime('%I:%M %p')
    print(current_time)
    engine.say(f"The time is {current_time}.")
    engine.runAndWait()


def search_wikipedia(query):
    """Searches Wikipedia for the given query"""
    speak('Searching Wikipedia...')  # Commented out as 'speak' is not defined
    results = wikipedia.summary(query, sentences=2)
    print(results)
    engine.say(f"According to Wikipedia, {results}")  # Modified to use engine.say
    engine.runAndWait()


def play_video(text):
    """Attempts to play a video on Youtube based on user input"""
    if 'play' in text:
        video_title = text.split('play', 1)[1].strip()  # Extract video title after "play"
    else:
        video_title = text  # Use full text if "youtube" is mentioned
    engine.say("Opening Youtube.")
    engine.runAndWait()
    try:
        pywhatkit.playonyt(video_title)
    except Exception as ex:
        print(f"Error playing video: {ex}")
        engine.say("Sorry, there might be a problem with Youtube.")
        engine.runAndWait()


if __name__ == "__main__":
    while True:
        listen_and_respond()
