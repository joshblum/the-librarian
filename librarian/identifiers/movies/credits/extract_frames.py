"""
    Extract the frames from the given video file and 
    put them in the given directory.
"""

from librarian.utils import get_time_delta
import subprocess
import shlex
import pipes
import re
import os

MIN = 5
MATCH_EXPR = "Duration: (?P<dur>.*), start:"
CUT_VID = "%s.cut.mp4"
FRAME_NAME = "%s/image-%%3d.png"
FRAMERATE = "0.15"


def extract_frames(filename, outdir, framepath):
    end_time = get_vid_len(filename)
    start_time = get_time_delta(end_time)
    cut = pipes.quote(os.path.join(outdir, CUT_VID % os.path.basename(filename)))
    frame = FRAME_NAME % framepath

    cut_vid(filename, cut, start_time, end_time)
    gen_frames(cut, frame)


def get_vid_len(filename):
    cmd = "ffprobe %(filename)s" % {
        'filename': filename
    }
    call = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
    return re.findall(MATCH_EXPR, call)[0]


def cut_vid(inname, outname, start_time, end_time):
    """
        Cut the video at the specified times copying 
        the video from the inname to outname
    """
    cmd = "ffmpeg -y -ss %(start_time)s -i %(inname)s -t %(end_time)s -c:v copy -c:a copy %(outname)s" % {
        'inname': inname,
        'outname': outname,
        'start_time': start_time,
        'end_time': end_time,
    }
    return subprocess.check_output(shlex.split(cmd))


def gen_frames(input_name, frame_name, framerate=FRAMERATE):
    """
        generate still frames for the given video with the 
        specified frame_name every 1/framerate seconds
    """
    cmd = "ffmpeg -y -i %(input_name)s -r %(framerate)s -f image2 %(frame_name)s" % {
        'input_name': input_name,
        'framerate': framerate,
        'frame_name': frame_name,
    }
    return subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)


if __name__ == "__main__":
    extract_frames('tmp/test.mp4', 'tmp')
