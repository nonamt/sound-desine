# *********************************************************
# 
# sound desine beta 0.7.1
#
# @author: Johanna Tiikkainen
# @author: Mikko Mäkitalo
#
# @date: 2023/02/05
# 
# **********************************************************

import math
import time
import numpy as np
import pyaudio

# all functions

# frames_to_buffer()
# counts the number of frames for the buffer if frequency != integer
# parameters: frequency (float), sampling_frequency (int?)
# returns: float

def frames_to_buffer(frequency, sampling_frequency):

    if not frequency.is_integer():

        integer_part = math.floor(frequency) # round down to the nearest integer
        frames = round(integer_part / frequency * sampling_frequency)

    else:
        frames = sampling_frequency

    return (frames)


# new_sine()
# plays a sine wave
# parameters: sampling rate fs (float), frequency (float), 
# volume (float), all_streams (dict)

def new_sine(fs, frequency, volume, all_streams):

    frames = frames_to_buffer(frequency, fs)

    samples = volume * (np.sin((2 * np.pi * np.arange(fs) * frequency) / fs)).astype(np.float32)

    # in callback mode, pyaudio calls a user-defined 
    # callback function when it needs new audio data to play
    # more: https://people.csail.mit.edu/hubert/pyaudio/docs/#example-callback-mode-audio-i-o

    def callback(in_data, frame_count, time_info, status):
        data = samples
        return (data, pyaudio.paContinue)

    # the stream is opened -> starts processing

    stream = p.open(format=pyaudio.paFloat32, 
                        channels=1, 
                        rate=fs, 
                        frames_per_buffer=frames, 
                        output=True,
                        stream_callback=callback)

    all_streams["counter"] += 1

    stream_name = "sine{}".format(all_streams["counter"])
    all_streams[stream_name] = stream

    print("\n{} f: {} v: {} droning\n".format(stream_name, frequency, volume))
    

# sine_break()
# stops a stream but doesn't close it
# parameters: name (str), all_streams (dict)

def sine_break(name, all_streams):

    if name not in all_streams:
        print("\n{} does not exist\n".format(name))
        return
    
    all_streams[name].stop_stream()

    print("\n{} is sleeping\n".format(name))


# sine_returns()
# plays a stopped stream
# parameters: name (str), all_streams (dict)

def sine_returns(name, all_streams):

    if name not in all_streams:
        print("\n{} does not exist\n".format(name))
        return

    all_streams[name].start_stream()

    print("\n{} lives again\n".format(name))


# stop_sine()
# stops a stream and closes it
# parameters: name (str), all_streams (dict)

def stop_sine(name, all_streams):

    if name not in all_streams:
        print("\n{} does not exist\n".format(name))
        return

    all_streams[name].stop_stream()
    all_streams[name].close()

    del all_streams[name]

    print("\n{} drones no more\n".format(name))


# terminate()
# stops and closes all existing streams
# parameters: all_streams (dict)
# todo: test with inactive streams

def terminate(all_streams):

    for name in all_streams:

        if len(all_streams) == 1:
            print("\nthere is nothing to terminate\n")
            return

        if name != "counter":
            all_streams[name].stop_stream()
            all_streams[name].close()
            print("")
            print("{} has been terminated".format(name))
    
    print("")

    # deletes the terminated streams from the dictionary
    for i in range(len(all_streams)):

        if "sine{}".format(i) in all_streams:
            del all_streams["sine{}".format(i)]
            # print("sine{}".format(i) + " deleted")


# todo: funktiokommentit
# 12-sävelinen tasavireinen asteikko

def tones(note):

    # the parameter is exctracted from the command "12 <note> <volume>"
    # e.g. with the input "12 c1 0.1" -> args[1] == "c1"
    # tones(args[1]) -> note: args[1] == "c1"

    scale = {"c": 32.70, "cs": 34.65, "d": 36.71, "ds": 38.89, 
              "e": 41.20, "f": 43.65, "fs": 46.25, "g": 49.00, 
              "gs": 51.91, "a": 55.00, "as": 58.27, "b": 61.74}

    octave = int(note[-1])-1 # -> 0, 1, 2 etc.
    tone = scale[note[:-1]] # -> "cs", "d"
    frequency = tone * (2 ** octave)

    return frequency


# help()
# prints the list of available commands

def help():

    print("\n// commands //")
    print("> exit") # poistuu ohjelmasta (jos avoimia streameja, sulkee ja lopettaa)
    print("> help") # tulostaa tämän ohjeen
    print("> new <frequency> <volume>") # todo: lisää komentojen kuvaukset
    print("> 12 <tone> <volume>") # 12-sävelinen tasavireinen asteikko
    print("> pause <stream_name>") # pysäyttää streamin <stream_name>
    print("> play <stream_name>") # jatkaa streamin <stream_name> toistoa
    print("> stop <stream_name>") # pysäyttää ja sulkee streamin <stream_name>
    print("> terminate\n") # pysäyttää ja sulkee kaikki avoimet streamit


# beginning of "main"

start = time.time()

# instantiate pyaudio and initialize portaudio system resources
p = pyaudio.PyAudio()

# sampling frequency
fs = 44100

# dict keys, values:
# counter, number of streams created
# for each stream: stream name, stream object
streams = {"counter": 0} 

print("\n\n              s o u n d  d e s i n e")
print("\n                     0.6.1-b")
print("\n              droned out / out-droned")
print("\n")

# help()

cmd = input("> ")

args = cmd.split()

while True:

    if args[0] == "new":
        new_sine(fs, float(args[1]), float(args[2]), streams)

    elif args[0] == "12":
        new_sine(fs, tones(args[1]), float(args[2]), streams)

    elif args[0] == "stop":
        stop_sine(args[1], streams)

    elif args[0] == "pause":
        sine_break(args[1], streams)
        
    elif args[0] == "play":
        sine_returns(args[1], streams)

    elif args[0] == "terminate":
        terminate(streams)

    elif args[0] == "exit":
        terminate(streams)
        break
    
    elif args[0] == "help":
        help()

    # todo: handling invalid input
    
    args.clear()
    cmd = input("> ")
    args = cmd.split()

print("the runtime is {:.2f}".format(time.time() - start))
print("\n{} sines played".format(streams["counter"]))

p.terminate()

print("\nsine-ing out\n")