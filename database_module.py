from requests import get
from json import loads, dumps
from pickle import loads as load_, dumps as dump_    
class Database():
    db_url = 'https://simpledatabase.pl608.repl.co/'
    def __init__(self):
        self.sid = loads(get(f'{self.db_url}').text).get('sid')
    def save(self, key:str, value:str):
        resp = loads(get(f'{self.db_url}/?key={key}&val={value}').text)
        if resp.get('saved',False)==False:
            raise KeyError(resp.get('error', 'No Error Returned'))
    def get(self, key):
        resp = loads(get(f'{self.db_url}/?key={key}'))
        if 'error' in resp:
            if key != 'error':
                raise KeyError(resp.get('error', 'No Error Returned'))
        return resp
    def __getitem__(self, key):
        return get(key)
    def append(self, key):
        self.save(key, None)
    def check_in(self, key):
        resp = loads(get(f'{self.db_url}/?sid={self.sid}&key={key}&cmd=in').text)
        if type(resp)==bool:
            return resp
        else:
            raise KeyError(resp.get('error', 'No Error Returned')) 

    
