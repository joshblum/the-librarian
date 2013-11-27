"""
    Movie credit identification handler.
    Create this object with an input file
"""

from identification_handler import IdentificationHandler

class MovieCreditIdentifier(IdentificationHandler):

    def __init__(self, srcfile):
        super(IdentificationHandler, self).__init__(srcfile)

    def indentify(self):

    def cleanup(self)

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
