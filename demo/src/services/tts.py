import pyttsx3

engine = pyttsx3.init()

engine.setProperty('rate', 150)  # Speed of speech (words per minute)
engine.setProperty('volume', 0.9) # Volume level (0.0 to 1.0)

voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[0].id) # For a male voice (index may vary)
# engine.setProperty('voice', voices[1].id) # For a female voice (index may vary)

# # Convert text to speech
# engine.say("Hello, this is a text-to-speech example using pyttsx3.")

# # Wait for the speech to complete
# engine.runAndWait()

# # Stop the engine
# engine.stop()

def say(text):
    engine.say(text)
    engine.runAndWait()
