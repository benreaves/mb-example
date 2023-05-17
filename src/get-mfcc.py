# read an audio file 1.wav and write it to 2.wav
# using the pyaudio library
#

# read input file
# read wav file using wav
from scipy.io import wavfile as wav
wf, fs = wav.read("../data/watermelon.wav")

print("sampling frequency is ", fs)

# calculate the mfcc
import python_speech_features
mfcc = python_speech_features.mfcc(wf, fs)

## root cause of the error: line 8 is in the wrong order! See
## https://python-speech-features.readthedocs.io
## should be fs,wf = wav.read("1.wav")
