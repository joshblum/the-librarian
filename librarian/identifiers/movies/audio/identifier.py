from librarian.constants import LOGGING
from librarian.identifiers.identifiers import MovieIdentifier
from extract_audio import *


import os
import logging.config

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


class MovieAudioIdentifier(MovieIdentifier):

    def __init__(self, srcfile, path):
        super(MovieIdentifier, self).__init__(srcfile, path)
        
        self.audio_path = "%s/audio" % self.path
        if not os.path.exists(self.audio_path):
            os.mkdir(self.audio_path)

    def get_audio_fingerprint(self):
        run_audio_extraction(self.srcfile, self.audio_path)
        logger.debug("Extracting audio...")
        audio_fingerprint = get_audio_fingerprint(self.srcfile)
        return audio_fingerprint

    def get_titles(self):
        audio_fingerprint = self.get_audio_fingerprint()
        metadata = self.metastore.find_metadata_by_fingerprint(audio_fingerprint)
        if metadata is None:
            return []
        #return [item['title'] for item in metadata['data']]

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        ident = MovieAudioIdentifier(sys.argv[1], "/tmp")
        print ident.identify()

