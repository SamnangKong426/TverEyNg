# import required module
import os

# play sound
file = "/home/user/Documents/TverEyNg/demo/app/assets/thief_sound.mp3"
print('playing sound using native player')
os.system("mpg123 " + file)