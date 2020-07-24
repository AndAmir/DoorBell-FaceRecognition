from gtts import gTTS
from pygame import mixer
import time
mixer.init()


def morning(names):
    for name in names:
        tts = gTTS(text="Good morning "+name+"", lang="en-au")
        tts.save("output.mp3")
        mixer.music.load('/Users/Andy/PycharmProjects/FaceRecognition/output.mp3')
        mixer.music.play()
        time.sleep(2)


def afternoon(names):
    for name in names:
        tts = gTTS(text=" Good afternoon "+name+"", lang="en-au")
        tts.save("output.mp3")
        mixer.music.load('/Users/Andy/PycharmProjects/FaceRecognition/output.mp3')
        mixer.music.play()
        time.sleep(2)


def evening(names):
    for name in names:
        tts = gTTS(text="Good evening "+name+"", lang="en-au")
        tts.save("output.mp3")
        mixer.music.load('/Users/Andy/PycharmProjects/FaceRecognition/output.mp3')
        mixer.music.play()
        time.sleep(2)


def speak(inputtxt):

    tts = gTTS(text=inputtxt, lang="en-au")
    tts.save("output.mp3")
    mixer.music.load('/Users/Andy/PycharmProjects/FaceRecognition/output.mp3')
    mixer.music.play()
    time.sleep(2)
