import subprocess
import shlex
import os
import time
import json
import sys

def extract_audio(input_name, output_name):
    cmd = "ffmpeg -i %(input_name)s -ab %(bitrate)s -ac %(channels)s -ar %(sampling_frequency)s -vn %(output_name)s" % {
        'input_name': input_name,
        'bitrate': '160k',
        'channels': '2',
        'sampling_frequency': '44100',
        'output_name': output_name
    }
    return subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)

def generate_data(input_name):
    cmd = "./echoprint-codegen %(filepath)s%(filename)s" % {
        "filepath": "/home/linux-laptop/Desktop/audioextract/",
        "filename": input_name
    }
    return subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)

def get_json(s):
    pre_json = format_text(s)
    return json.loads(pre_json)

def format_text(s):
    o = s.strip('\n')
    o = o[1:len(o)-1]
    return o

def get_audio_fingerprint(pathtofile, input_name):
    print "Getting audio fingerprint.."
    video_file = pathtofile + input_name
    #r = str(time.time())
    print "Generating audio..."
    audio_output = "tmp/tmp-output" # + r
    extract_audio(video_file, audio_output + ".mp3")
    print "Done."
    print "Renaming file..."
    os.rename(audio_output + ".mp3", audio_output)
    print "Done.."
    print "Generating data..."
    jsonData = get_json(generate_data(audio_output))
    print "Done."
    code = jsonData["code"]
    f = open("results/" + input_name, "w")
    print "Writing code..."
    f.write(code)
    print "Done.."
    print "Cleaning up..."
    f.close()
    os.remove(audio_output)
    print "Done."

#ffmpeg -i korrabackup -vcodec copy -acodec copy -ss 00:00:00 -t 00:00:30 shortkorra.avi

def split_movie(pathtofile, input_name, start_time="00:00:00", end_time="00:00:30"):
    video_file = pathtofile + input_name
    cmd = "ffmpeg -i %(video_file)s -vcodec copy -acodec copy -ss %(start)s -t %(end)s %(output_name)s" % {
        'video_file': video_file,
        'start': start_time,
        'end': end_time,
        'output_name': pathtofile + "splits/short-" + input_name + str(time.time()) + ".avi"
    }
    return subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)

def split_movie_by_increments(pathtofile, input_name, increments):
    pass
    
if __name__ == "__main__":   
    get_audio_fingerprint("files/","manofsteelsource")
    #split_movie("files/","korrasource")
