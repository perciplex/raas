from flask import Flask, jsonify, request, render_template
app = Flask(__name__)
from collections import namedtuple
from enum import Enum


class Status(str, Enum):
    QUEUED = 'QUEUED'
    RUNNING = 'RUNNING'
    COMPLETE = 'COMPLETE'

jobs = [{'gist':"test", 'status':Status.QUEUED}]


@app.route('/jobs', methods=['GET','POST'])
def jobs_route():
    print(request.form)
    if request.method == 'POST':
        jobs.append({'gist':request.form['gist'], 'status':Status.QUEUED})
        return render_template('jobs.html', jobs=jobs)
    if request.method == 'GET':
        return jsonify(list(filter(lambda job: job['status']==Status.QUEUED, jobs)))


@app.route('/')
def base_route():
    return render_template('jobs.html', jobs=jobs)