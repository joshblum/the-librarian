from librarian.constants import LOGGING
from librarian.identifiers.identifiers import MovieIdentifier
from extract_audio import fingerprint_for_file

import os
import logging.config

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


class MovieAudioIdentifier(MovieIdentifier):

    def __init__(self, srcfile, path, fingerprint=None):
        super(MovieIdentifier, self).__init__(srcfile, path)

        self.audio_path = "%s/audio" % self.path
        if not os.path.exists(self.audio_path):
            os.mkdir(self.audio_path)

        if fingerprint is None:
            fingerprint = fingerprint_for_file(self.audio_path,
                                               self.srcfile)

        self.fingerprint = fingerprint

    def get_titles(self):
        return None

    def get_title_metadata(self, titles):
        return self.metastore.find_metadata_by_fingerprint(self.fingerprint)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        ident = MovieAudioIdentifier(sys.argv[1], "/tmp")
        print ident.identify()
