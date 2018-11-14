 #!flask/bin/python
from flask import Flask, jsonify
from task import processFile
from task import keywords

BASEDIR="data/"
results = []

            
# CELERY_URL = "amqp://localhost"
# CELERY_BACKEND = os.environ['CELERY_RESULT_BACKEND']        

app = Flask(__name__)
# celery_app = celery.Celery(
#     "task", broker=CELERY_URL)

@app.route('/start', methods=['GET'])
def start():
    import os
    tasks = []
    for f in os.listdir(BASEDIR):
        fname = os.path.join(BASEDIR, f)
        res = processFile.delay(fname)        
        tasks.append(res)
    group = celery.group(tasks)()
    group.save()
    return(str(group))

@app.route('/done', methods=['GET'])
def done():
    doneCount = 0
    output = "<table><tr>"
    for r in results:
        if r.ready():
            output += "<tr><td>" + str(r) + "</td><td>RDY</td></tr>"
            doneCount += 1
        else:
            output += "<tr><td>" + str(r) + "</td><td>PND</td></tr>"            

    header = "<h1>" + str(doneCount) + "/" + str(len(results)) + "</h1>"
    return(header + "<br>" + output)

@app.route('/results', methods=['GET'])
def get_tasks():
    completed = True
    total = {}
    for r in results:
        if r.ready():
            counts = r.get()
            for k in keywords:
                total[k] = total.get(k, 0) + counts.get(k, 0)
        else:
            completed = False

    table = "<table>"
    for k in keywords:
        table += "<tr><td>" + k + "</td><td>" + str(total.get(k,0)) + "</td></tr>"
    table += "</table>"
    if completed:
        return("<h1>DONE!</h1><br>" + table)
    else:
        return("<h1>Pending...</h1><br>" + table)    

def start():
    import os
    for f in os.listdir(BASEDIR):
        fname = os.path.join(BASEDIR, f)
        res = processFile.delay(fname)
        results.append(res)


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=80,debug=True)
