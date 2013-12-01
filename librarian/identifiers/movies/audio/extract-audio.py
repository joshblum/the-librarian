import subprocess
import shlex
import os
import time
import json

def gen_audio(input_name, output_name):
    cmd = "ffmpeg -i %(input_name)s -ab %(bitrate)s -ac %(channels)s -ar %(sampling_frequency)s -vn %(output_name)s" % {
        'input_name': input_name,
        'bitrate': '160k',
        'channels': '2',
        'sampling_frequency': '44100',
        'output_name': output_name
    }
    return subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)

def generate_data(input_name):
    cmd = "./echoprint-codegen %(filepath)s" % {
        "filepath": "/home/linux-laptop/Desktop/audioextract/tmp/song.mp3"
    }
    return subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)

def get_json(s):
    pre_json = format_text(s)
    return json.loads(pre_json)

def format_text(s):
    o = s.strip('\n')
    o = o[1:]
    o = o[:-1]
    return o

if __name__ == "__main__":
    r = str(time.time())
    output = "tmp/tmp-output" + r + ".mp3"
    jsonData = get_json(generate_data("tmp/tmp-output"))
    md = jsonData["metadata"]
    code = jsonData["code"]
    print code
