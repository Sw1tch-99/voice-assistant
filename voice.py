import pyttsx3 as p
import speech_recognition as sr
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import datetime


engine = p.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', 180)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # voice[1] for female and voice[0] for male

def speak(text):
    engine.say(text)
    engine.runAndWait()


r = sr.Recognizer()

# Voice Assistant Introduction
speak("Hello ma'am, I am your voice assistant. How are you?")

def recognize_speech():
    with sr.Microphone() as source:
        r.energy_threshold = 3000
        r.adjust_for_ambient_noise(source, duration=1.2)
        print("Listening...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            speak("Sorry, I did not catch that. Could you please repeat?")
            return recognize_speech()
        except sr.RequestError:
            speak("Sorry, I am having trouble connecting to the recognition service.")
            return None


text = recognize_speech()
if text and "what" in text and "about" in text and "you" in text:
    speak("I am having a good day ma'am. What can I do for you?")


text2 = recognize_speech()

if text2:
    if "information" in text2:
        speak("You need information related to which topic?")
        
        infor = recognize_speech()
        if infor:
            # Define the Infow class
            class Infow:
                def __init__(self):
                    # Assuming chromedriver is in PATH, else provide the full path to the chromedriver
                    self.driver = webdriver.Chrome()

                def get_info(self, query):
                    self.driver.get("https://www.wikipedia.org")
                    search_box = self.driver.find_element(By.XPATH, '//*[@id="searchInput"]')
                    search_box.send_keys(query + Keys.RETURN)

            
            assist = Infow()
            assist.get_info(infor)

            
            input("Press Enter to close the browser...")
            assist.driver.quit()

    elif "time" in text2:
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        speak(f"The current time is {current_time}")

    elif "date" in text2:
        today = datetime.date.today()
        speak(f"Today's date is {today.strftime('%B %d, %Y')}")

    else:
        speak("Sorry, I didn't understand that. Please try again.")
else:
    speak("Sorry, I didn't understand that. Please try again.")
