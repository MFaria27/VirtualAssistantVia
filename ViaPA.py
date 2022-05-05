import speech_recognition
import pyttsx3
import webbrowser
import time
import subprocess

startup_message = "Starting Personal Assistant Via\n"

# Create "Via", the voice
via = pyttsx3.init()
voices = via.getProperty('voices')
rate = via.getProperty('rate')
via.setProperty('voice', voices[2].id)

# Find out the number of the next log using "count.txt"
# One is created everytime Via starts up, and will contain everything said to Via
history = open("history/count.txt", "r")
log_count = int(float(history.read()))
history = open("history/count.txt", "w")
history.write(str(log_count+1.0))
history.close()

# Create the new log
new_history_log = "history/log" + str(log_count) + ".txt"
log = open(new_history_log, "w")
log.write("Start of Log " + str(log_count) + "\n")

chrome_searchbar = "https://www.google.com/search?q="
brave_searchbar = "https://search.brave.com/search?q="

# Select which browser to use for search queries
browser = brave_searchbar

# Log and use text-to-speech whatever the message is
def tts(what_to_say):
    print(what_to_say)
    log.write(what_to_say + "\n")
    via.say(what_to_say)
    via.runAndWait()

# Listen to the microphone for a message to Via
def voice_command():

    # Initialize a voice recognizer
    recognizer = speech_recognition.Recognizer()

    # Only listen if a microphone is detected
    with speech_recognition.Microphone() as microphone:
        recognizer.pause_threshold = 1
        recognizer.adjust_for_ambient_noise(microphone)
        print("Listening...")
        speech_audio = recognizer.listen(microphone)

        try:
            # Use google's speech recognition to turn the message into a string to be analyzed
            heard = recognizer.recognize_google(speech_audio)
            heard = heard.lower()

            # Only continue if "Via" was said in the message, everything else is ignored
            if "via" in heard:
                print("Heard: " + heard)
                log.write("Heard: " + heard + "\n")
            else:
                return "None"
        except Exception as e:
            # If nothing is heard from the microphone, continue
            #print("Nothing heard")
            return "None"

        return heard

if __name__ == '__main__':
    
    tts(startup_message)

    while True:
        
        # Listen and return a message to Via
        command = voice_command()

        if command == 0:
            log.write("\n")
            continue

        # Turn Via off
        if ("bye" in command) or ("end" in command) or ("good night" in command) or ("goodnight" in command) or ("goodbye" in command) or ("leave" in command):
            tts("Going to sleep, Goodnight.")
            break
        
        # Turn computer off (Use "abort" command to stop)
        if ("turn off" in command):
            tts("Turning off your computer in 30 seconds, please tell me to abort if this was a mistake.")
            tts("See you next time.")
            subprocess.call(["shutdown", "/s", "/t", "30"])
            log.write("\n")
        
        # Restart computer (Use "abort" command to stop)
        elif ("restart" in command):
            tts("Restarting your computer in 30 seconds, please tell me to abort if this was a mistake.")
            tts("See you soon.")
            subprocess.call(["shutdown", "/r", "/t", "30"])
            log.write("\n")

        # Stops shutdown or restart command
        elif ("abort" in command):
            tts("Aborting shutdown process. That was close.")
            subprocess.call(["shutdown", "/a"])
            log.write("\n")

        # Opens youtube in browser
        elif ("open youtube" in command):
            tts("Opening YouTube in your browser")
            webbrowser.open_new_tab("https://www.youtube.com")
            log.write("\n")
        
        # Looks up a video in youtube
        elif ("in youtube look up" in command):
            command = command[command.index("up") + 3:len(command)]
            query = command
            command = command.replace(" ", "+")
            command = "https://www.youtube.com/results?search_query=" + command
            tts("Looking up " + query + " in YouTube")
            webbrowser.open(command, new = 2)
            log.write("\n")

        # Search for a query in your selected browser
        elif ("search" in command) or ("look up" in command) or ("lookup" in command):
            if ("search" in command):
                command = command[command.index("search") + 7:len(command)]
                query = command
                command = command.replace(" ", "+")
                command = browser + command
            if ("up" in command):
                command = command[command.index("up") + 3:len(command)]
                query = command
                command = command.replace(" ", "+")
                command = browser + command
            tts("Looking up " + query)
            webbrowser.open_new_tab(command)
            log.write("\n")
        
        # Search for a "what is" question in your selected browser
        elif ("what is" in command):
            command = command.replace("via", "")
            question = command
            command = command.replace(" ", "+")
            command = browser + command
            tts("Asking the internet" + question)
            webbrowser.open_new_tab(command)
            log.write("\n")

        time.sleep(0.1)