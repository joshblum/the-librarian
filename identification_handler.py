"""
    Abstract class for an identification handler.
    Requires a filename on object creation.
    Requires an identify and  cleanup method.
"""
from constants import ROOT_PATH

import uuid


class IdentificationHandler(object):

    def __init__(self, srcfile):
        self.srcfile = srcfile
        self.work_path = self.create_workspace()

    def create_workspace(self):
        """
            create a directory and return the absolute path
        """
        dirname = str(uuid.uuid4())
        path = os.path.join(ROOT_PATH, dirname)
        os.mkdir(path)
        return path

    def identify(self):
        raise NotImplementedError

    def cleanup(self):
        raise NotImplementedError
