from json import dump, load
from requests import get    
from bs4 import BeautifulSoup
from time import sleep
from threading import active_count as activeCount
from threading import Thread as t
from database_module import Database
import _thread
thread_que = []
class Thread():
    def __init__(self, target=None, args=()):
        self.target = target
        self.args = args
    def start(self):
        thread_que.append(lambda: self.target(*self.args))

start_url = "https://www.wikipedia.org/"
domains_db = Database()
pages_db = Database()
domains = []
pages = []
fails = []
def get_domain(url):
    #print(url)
    return url.split('/')[2]
def scan(url, parent):
    global domains, pages, domains_db, pages_db
    try:
        page = get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        for link in soup.findAll('a'):
            new_url = link.attrs.get('href')
            if new_url != None:
                if new_url.startswith('http'):
                    domain = get_domain(new_url)
                    if  domain not in domains:
                        domains_db.save(domain, parent)
                        domains.append(domain)
                        Thread(target=scan, args=(new_url, url)).start()
                else:
                    url_ = f"{url}{new_url}"
                    if url_ not in pages == False:
                        pages.append(url_)
                        pages_db.save(url_, parent)
                        Thread(target=scan, args=(url_, url)).start()
            #print(link.attrs.get('href'))
    except Exception as e:
        print(e)
        fails.append((url, str(e)))
def thread_handler():
    global thread_que
    while True:
        if activeCount() <= 10:
            if thread_que.__len__() > 0:
                print(1)
                t(target=thread_que.pop(0)).start()
t(target=lambda:scan(start_url, start_url), name='scanner').start()
t(target=thread_handler).start()
while True:
    sleep(1)
