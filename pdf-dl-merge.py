# -*- coding: utf-8 -*-
#!/usr/bin/env python
import os
import sys
import requests
import datetime
import logging 
from settings import CACHE_DIR, FILENAME_FORMAT, REMOTE_FILES, URL_FORMAT, PDF_VIEWER
from subprocess import call
from PyPDF2 import PdfFileMerger, PdfFileReader
    

log = logging.getLogger("pdf-dl-merge")

def Main():
    today = datetime.date.today()
    year, week, wday = datetime.date.isocalendar(today)
    LOCAL_FILENAME = os.path.join(CACHE_DIR, FILENAME_FORMAT.format(week=week))
    
    if not os.path.isfile(LOCAL_FILENAME):
        log.info('Local PDF file not found.')
        
        for remote in REMOTE_FILES:
            with open(os.path.join(CACHE_DIR, remote), 'wb') as handle:
                url = URL_FORMAT.format(remotefile=remote)
                
                log.info('Getting remote file with url: {url}'.format(url=url))
                r = requests.get(url, stream=True)
                
                log.info('Writing local file')
                for block in r.iter_content(1024):
                    if not block:
                        break
                    
                    handle.write(block)
                log.info('Done')
                
        log.info('Merging PDFs:')
        merger = PdfFileMerger()
        
        for remote in REMOTE_FILES:
            merger.append(PdfFileReader(file(os.path.join(CACHE_DIR, remote), 'rb')))
        
        merger.write(LOCAL_FILENAME)       
        log.info('Done')
                    
    try:
        log.info('Openning merged PDF')
        call([PDF_VIEWER, LOCAL_FILENAME,])
    except:
        log.error('Fail to PDF file {weekpdffile}'.format(weekpdffile=FILENAME_FORMAT.format(week=week)))


if __name__ == "__main__":
    Main()
