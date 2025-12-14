# import required modules
from pydub import AudioSegment
from pydub.playback import play
from threading import Thread

def play_sound():
    song = AudioSegment.from_mp3("assets/thief_sound.mp3")
    print('playing sound using  pydub')
    play(song)

def play_sound_async():
    Thread(target=play_sound, daemon=True).start()

if __name__ == "__main__":
    play_sound()