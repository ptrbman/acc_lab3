from celery import Celery
import json
import os

MASTER_IP = os.environ['MASTER_IP']
BACKEND = os.environ['CELERY_BACKEND']
BROKER = os.environ['CELERY_BROKER']

app = Celery('task', backend=BACKEND, broker=BROKER)
BASEDIR = "testdata/"


keywords = ["han", "hon", "den", "det", "denna", "denne", "hen"]

def analyze(text, wordCounts):
    for word in text.split():
        if word in keywords:
            wordCounts[word] = wordCounts.get(word, 0) + 1

@app.task            
def processFile(fname):
    os.system('scp "%s:%s" "%s"' % (fname, MASTER_IP, fname) )
    wordCounts = {}
    f = open(fname, "r")
    for l in f:
        if l.strip() != "":
            js = json.loads(l)
            if js['retweeted'] == False:
                analyze(js['text'], wordCounts)
    return wordCounts
