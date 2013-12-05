import os
import logging
from logging import FileHandler, StreamHandler


# SETTINGS:

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
CACHE_DIR = os.path.join(BASE_DIR, 'cachedir')

REMOTE_FILES = (
    'file1.pdf',
    'file2.pdf',
    'file3.pdf',
)
FILENAME_FORMAT = 'pdffile-{week}.pdf'

URL_MENU = 'http://example.com/pdf/{remotefile}'

PDF_VIEWER = "evince"


#  LOG:
default_formatter = logging.Formatter(\
   "%(asctime)s:%(levelname)s:%(message)s")

console_handler = StreamHandler()
console_handler.setFormatter(default_formatter)

error_handler = FileHandler("error.log", "a")
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(default_formatter)

root = logging.getLogger()
root.addHandler(console_handler)
root.addHandler(error_handler)
root.setLevel(logging.DEBUG)
