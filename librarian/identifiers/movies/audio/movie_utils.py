import subprocess
import shlex
import os
import time
import json
import sys

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
    video_file = pathtofile + input_name

def add_time(time, time_to_add):
    hrs, mins, secs = time.split(":")
    secs, carry = add_and_carry(secs, time_to_add)
    mins, carry = add_and_carry(mins, carry)
    hrs = int(hrs) + carry
    return "%s:%s:%s" % (stringify(hrs), stringify(mins), stringify(secs))

def add_and_carry(value, value_added):
    val = int(value) + int(value_added)
    return (val % 60, val / 60)

def stringify(d):
    if d < 10:
        return "0%s" % d
    else:
        return "%s" % d
    print hrs

if __name__ == "__main__":   
    pass