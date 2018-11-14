 #!flask/bin/python
from flask import Flask, jsonify
from task import processFile
from task import keywords
import task
import celery

BASEDIR="data/"

app = Flask(__name__)

@app.route('/start', methods=['GET'])
def start():
    import os
    tasks = []
    for f in os.listdir(BASEDIR):
        fname = os.path.join(BASEDIR, f)
        res = processFile.s(fname)        
        tasks.append(res)
    group = celery.group(tasks)()
    group.save()
    return(str(group))

@app.route('/done/<string:id>', methods=['GET'])
def done(id):
    group = task.app.GroupResult.restore(id)
    output = ""
    allDone = True
    for r in group:
        output += r.state + "<br>"
        if not (r.state == "SUCCESS"):
            allDone = False
    if allDone:
        return("True")
    else:
        return("False")

    @app.route('/results/<string:id>', methods=['GET'])
def get_tasks(id):
    group = task.app.GroupResult.restore(id)
    total = {}
    for r in group:
        print(r)
        if r.state == "SUCCESS":
            print("\tReady")
            counts = r.get()
            for k in keywords:
                total[k] = total.get(k, 0) + counts.get(k, 0)

    table = "<table>"
    for k in keywords:
        table += "<tr><td>" + k + "</td><td>" + str(total.get(k,0)) + "</td></tr>"
    table += "</table>"

    return(table)


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=80,debug=True)
