import atexit
import logging
import increasmentdownload
import html_downloader_requests
import esimporter
import esimporter_html
import apiservice
import threading
import time
import subprocess
import webbrowser

from log import Log

WEB_PROCESS = None
ES_PROCESS = None
API_PROCESS = None


def start_backend_to_fetch_data():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s.%(msecs)03d %(levelname)s %(filename)-8s: %(lineno)s line -%(message)s',
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    while True:
        try:
            increasmentdownload.increasement_download()
            html_downloader_requests.download_htmls()
            esimporter.ESImporter().import_to_db()
            esimporter_html.ESImporterFromHTMLContent().import_to_db()
        except Exception as e:
            logging.exception(f"Error in main_flow.py: {e}")
        time.sleep(10 * 60)  # sleep for 10 minutes


def start_api_server():
    # threading.Thread(target=apiservice.run_app).start()

    global API_PROCESS
    API_PROCESS = subprocess.Popen(['start-api.bat'])


def start_es():
    # threading.Thread(target=start_es)
    # def start ():    
    '''
    current.health="YELLOW" message="Cluster health status changed from [RED] to [YELLOW] (reason: [shards started [[.slo-observability.summary-v2][0], [.kibana-observability-ai-assistant-conversations-000001][0], [.apm-source-map][0]]])." previous.health="RED" reason="shards started [[.slo-observability.summary-v2][0], [.kibana-observability-ai-assistant-conversations-000001][0], [.apm-source-map][0]]"
    '''
    global ES_PROCESS
    ES_PROCESS = subprocess.Popen(['start-es.bat'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    while True:
        output = ES_PROCESS.stdout.readline()
        if output == '' and ES_PROCESS.poll() is not None:
            break
        if output:
            print(output.strip())
            if b'current.health="YELLOW" message="Cluster health status changed from [RED] to [YELLOW]' in output:
                break
            
def start_browser():            
    webbrowser.open("http://localhost:5173/" )


def start_web():
    global WEB_PROCESS
    WEB_PROCESS = subprocess.Popen(['start-web.bat'])


def stop_services():
    processes_to_stop = [WEB_PROCESS, API_PROCESS, ES_PROCESS]
    for process in processes_to_stop:
        if process:
            print(f"Stopping service... {process.pid}")
            try:
                process.kill()
            except:
                print('stop service failed')

def start_services():
    # Log.setup()
    start_web()
    start_es()
    start_api_server()
    start_browser()
    atexit.register(stop_services)
    start_backend_to_fetch_data()
    while True:
        time.sleep(10 * 60)  # sleep for 10 minutes


if __name__ == '__main__':
    start_services()
