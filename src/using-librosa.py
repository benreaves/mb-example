# read an audio file 1.wav and write it to 2.wav
# using the pyaudio library
#
# import the pyaudio library
## but you didn't use it! and it has a problem https://stackoverflow.com/questions/33513522/ )

#import pyaudio
# import the wave library
import wave, numpy

# parse args -i inputfile -o outputfile
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--inputfile", help="input file", default="1.wav")
parser.add_argument("-o", "--outputfile", help="output file", default="2.wav")
args = parser.parse_args()

# read input wav file using wave
## from scipy.io import wavfile as wav
import scipy.io.wavfile as wav
wf, fs = wav.read(args.inputfile)
## retvals are in the wrong order!

# read input file of any audio format
import soundfile as soundfile
wf, fs = soundfile.read(args.inputfile)
print(fs)
## great, it's in the right order!
## but it can not read an mp3 file :(

# read input file of mp3 format
import librosa
wf, fs = librosa.load(args.inputfile)
print(fs)
## great, it's in the right order!
print(wf)
# convert wf to mono
if wf.shape[1] == 2: # input was stereo
    wf = .5*(wf[:,0] + wf[:,1])

librosa.output.write_wav(args.outputfile, wf, fs)