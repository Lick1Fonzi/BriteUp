import os
from pprint import pprint
from preprocessor import preprocess

enc = 'utf-8'
class extractor:
    def __init__(self,path):
        self.path = path
    
        self.extract()

    def extract(self):
        with open(self.path,encoding=enc) as f:
            raw_lines = [line for line in f.read().splitlines()]
            lines = [line for line in raw_lines if line]

        self.url = lines[0]
        self.event_name = lines[1]
        self.date = lines[2]
        self.content = str(lines[4:])

    def __str__(self):
        return "URL:\n{0}\nEVENT NAME:\n{1}\nPATH:\n{2}\n".format(self.url,self.event_name,self.path)

def lista_documenti():
    path = '../Docs/'
    return [path+d+'/'+f for d in os.listdir(path) for f in os.listdir(path+d)]

