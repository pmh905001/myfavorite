

import logging
import increasmentdownload
import html_downloader_requests
import esimporter


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s.%(msecs)03d %(levelname)s %(filename)-8s: %(lineno)s line -%(message)s',
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    increasmentdownload.increasement_download()
    html_downloader_requests.download_htmls()
    esimporter.ESImporter().import_to_db()
    
