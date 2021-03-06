from librarian.constants import LOGGING
from movie_utils import split_movie
import subprocess
import shlex
import pipes
import os
import json
import sys
import logging.config

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


def run_audio_extraction(srcfile, audio_path):
    video_file = srcfile
    output = "%s/%s" % (audio_path, "audio-output")
    audio_file = "%s.mp3" % output
    extract_audio(video_file, audio_file)
    os.rename(audio_file, output)
    return output


def get_audio_fingerprint(srcfile):
    audio_file = srcfile
    jsonData = get_json(run_echoprint(audio_file))
    code = jsonData["code"]
    return code


def extract_audio(input_name, output_name):
    cmd = "ffmpeg -y -i %(input_name)s -ab %(bitrate)s -ac %(channels)s -ar %(sampling_frequency)s -vn %(output_name)s" % {
        'input_name': input_name,
        'bitrate': '160k',
        'channels': '2',
        'sampling_frequency': '44100',
        'output_name': output_name
    }
    return subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)


def run_echoprint(input_name):
    cmd = "echoprint-codegen %(filename)s" % {
        "filename": input_name
    }
    return subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)


def get_json(s):
    pre_json = format_text(s)
    return json.loads(pre_json)


def format_text(s):
    o = s.strip('\n')
    o = o[1:len(o) - 1]
    return o


def fingerprint_for_file(path, srcfile):
    srcfile = pipes.quote(srcfile)
    short_movie = "%s/short.avi" % path
    split_movie(srcfile, short_movie)
    run_audio_extraction(short_movie, path)
    logger.debug("Extracting audio...")
    audio_fingerprint = get_audio_fingerprint(short_movie)
    return audio_fingerprint

if __name__ == "__main__":
    print ROOT_PATH
    pass
    #extract_audio( "path to the movie file", "path to the movie file .mp3")
