# read an audio file 1.wav and write it to 2.wav

#import pyaudio
# import the wave library
import wave

# parse args -i inputfile -o outputfile
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--inputfile", help="input file", default="1.wav")
parser.add_argument("-o", "--outputfile", help="output file", default="2.wav")
args = parser.parse_args()

# read input file
## wf = wave.open(args.inputfile, 'rb')
## no it should be wav.read()
# read wav file using wav
from scipy.io import wavfile as wav
wf, fs = wav.read(args.inputfile)

samplerate, wf = wav.read(args.inputfile)
print(samplerate)

# read any format audio file
import soundfile as soundfile
wf, samplerate = soundfile.read(args.inputfile)


# calculate the mel frequency cepstral coefficients in 10ms frames into a pandas dataframe
# using the python_speech_features library
#
# import the python_speech_features library
import python_speech_features
# import the pandas library
import pandas

# read file "1.wav"
## AttributeError: module 'python_speech_features' has no attribute 'wav'
## (wf, fs) = python_speech_features.wav.read("1.wav")

# calculate the mfcc
mfcc = python_speech_features.mfcc(wf, samplerate)


# save the mfcc to a pandas dataframe
df = pandas.DataFrame(mfcc)

# write the df to a csv file
df.to_csv("1.csv", index=False)

# normallize each column of the dataframe
df2 = (df - df.mean()) / (df.max() - df.min())

## oops, that's not what I meant 

# normallize each column of the dataframe to zeromean and unit variance
df = (df - df.mean()) / df.std()

# calculate the distance between each row of the dataframe
# using the euclidean distance
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.cdist.html
from scipy.spatial import distance
dist = distance.cdist(df, df, 'euclidean')

## that's not quite right it is:
spectral_similarity = ss = dist[0]

# plot two dataframes on the same axis
# https://stackoverflow.com/questions/22219004/grouping-data-in-pandas-pyplot


# now plot wf and ss on the same time axis
import matplotlib.pyplot as plt
import numpy as np, math

# return a list of all elements of wf that are greater than 0, and 0 otherwise

# plot the wave and the spectral similarity
plt.plot([i/samplerate for i in range(len(wf))], [max(1,w) for w in wf])
total_time = tt = len(wf)/samplerate
plt.plot([i*tt/len(ss) for i in range(len(ss))], ss)
plt.yscale('log')


#df_wav = pandas.DataFrame({'wave':wf})
# plot df_wav to pdf
#df_wav.plot(x=[i/fs for i in range(len(wf))])
plt.savefig("1.pdf")
#
#df_ss  = pandas.DataFrame({'time':[i*tt/len(ss) for i in range(len(ss))], 'ss':spectral_similarity})
#df_wav.plot(x=[i/fs for i in range(len(wf))])

# get ready to chop: make a dataframe with 2 columns: time and spectral similarity to previous frame.
# put a time axis on both wav and ss, then combine them.
df_wav = pandas.DataFrame({'time':[i/samplerate for i in range(len(wf))], 'wave':wf})
df_ss  = pandas.DataFrame({'time':[(i+.5)*tt/len(ss) for i in range(len(ss))], 'ss':spectral_similarity})
print(df_ss.describe())
print("start df_combined")
# def f(row): # append the corresponding ss
#     t = row['time']
#     # find the first row in df_ss where time > t
#     row['ss'] = df_ss.query('time > @t').iloc[0]['ss']
#     return row
# df_combined = df_wav.apply(f, axis=1)

# df_combined.plot()
# plt.savefig("2.pdf")

import tqdm
ss_index = 0
ss_nexttime = df_ss.iloc[ss_index+1]['time']
ss = df_ss.iloc[ss_index]['ss']
print(df_ss.sample(20))
print(df_wav.sample(20))

rows = []
for i,r in tqdm.tqdm(df_wav.iterrows(), total=len(df_wav)):
    t = r['time']
    if t > ss_nexttime:
        if ss_index < len(df_ss) - 2:
            ss_index += 1
            ss_nexttime = df_ss.iloc[ss_index+1]['time']
            ss = df_ss.iloc[ss_index]['ss']
        elif ss_index == len(df_ss) - 2:
            ss_index += 1
            ss_nexttime = ss_nexttime * 2 # big. so we never get here again
            ss = df_ss.iloc[ss_index]['ss']
        elif ss_index == len(df_ss) - 1:
            # dont increment ss_index any more
            ss_nexttime = ss_nexttime * 2 # super big!
            ss = df_ss.iloc[ss_index]['ss']
    row = r.copy()
    row['ss'] = ss
    rows.append(row)
df_combined = pandas.DataFrame(rows)
print("done df_combined")
df_combined.to_pickle("dfcombined.pkl")
print(df_combined.sample(20))

# find the median of 

# looks like 25%tile of ss was 2.66, so let's set a threshold of 2.66

median = df_combined['ss'].median()
print("median ss is", median)
df_chopped = df_combined.query('ss > @median')
w = df_chopped['wave'].values.astype('int16')
# write w to 2.wav
soundfile.write(args.outputfile, w, samplerate)
