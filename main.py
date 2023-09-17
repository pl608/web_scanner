from json import dump, load
from requests import get    
from bs4 import BeautifulSoup
from time import sleep
from threading import active_count as activeCount
from threading import Thread as t
import _thread
class Thread():
    def __init__(self, target=None, args=None):
        self.target = target
        self.args = args
    def start(self):
        _thread.start_new_thread(target=self.target, args=self.args)
start_url = "https://www.wikipedia.org/"
domains = []
fails = []
def get_domain(url):
    #print(url)
    return url.split('/')[2]
def scan(url, parent):
    global domains
    try:
        page = get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        for link in soup.findAll('a'):
            sleep(.5)
            new_url = link.attrs.get('href')
            if new_url != None:

                if new_url.startswith('http'):
                    if new_url not in domains:
                        domains.append(new_url)
                        Thread(target=scan, args=(new_url, url)).start()
                else:
                    url_ = f"{url}{new_url}"
                    Thread(target=scan, args=(url_, url)).start()
            #print(link.attrs.get('href'))
    except Exception as e:
        fails.append((url, str(e)))
t(target=lambda:scan(start_url, start_url)).start()
while True:
    sleep(1)
    #print((activeCount()))
    t(target=lambda: dump(domains, open('domains.json', 'w'), indent=1)).start()
    t(target=lambda: dump(domains, open('fails.json', 'w'), indent=1)).start()
    #exit()
