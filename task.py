from celery import Celery
import json

app = Celery('task', backend='amqp', broker='amqp://')
BASEDIR = "testdata/"


keywords = ["han", "hon", "den", "det", "denna", "denne", "hen"]

def analyze(text, wordCounts):
    for word in text.split():
        if word in keywords:
            wordCounts[word] = wordCounts.get(word, 0) + 1

@app.task            
def processFile(fname):
    wordCounts = {}
    f = open(fname, "r")
    for l in f:
        if l.strip() != "":
            js = json.loads(l)
            analyze(js['text'], wordCounts)
    return wordCounts
