IMAGE_TEMPLATE = "image-%03d.png"
FPS = 1
API_KEY = "04a87a053afac639272eefbb94a173e4"


def generate_frames(video_filename, out_filename, fps=FPS):
    """
        generate the frames for the given video_filename into .png images
        ffmpeg -i test.avi -r 15 -s vga -f image2 image-%3d.png
    """
    subprocess.check_call(["ffmpeg", "-ss", "" "-i", video_filename,
                           "-r", str(fps), "-s", "vga", "-f", "image2", out_filename])


def _create_path():
    """
        create a directory and return the absolute path
    """
    dirname = str(uuid.uuid4())
    path = os.path.join(ROOT_PATH, dirname)
    os.mkdir(path)
    return path


if __name__ == "__main__":
    path = _create_path()
    generate_frames("test.avi", os.path.join(path, IMAGE_TEMPLATE))
