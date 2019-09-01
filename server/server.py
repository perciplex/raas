from flask import Flask, jsonify, request, render_template, redirect, make_response
app = Flask(__name__)
from collections import namedtuple
from enum import Enum
import uuid


class Status():
    QUEUED = 'QUEUED'
    RUNNING = 'RUNNING'
    COMPLETE = 'COMPLETE'

class Job:
    def __init__(self, git):
        self.id = uuid.uuid1()
        self.git = git
        self.status = Status.QUEUED
        self.results = "Results pending."
    def __dict__(self):
        return {"id": self.id, "results":self.results, "status":self.status}
    def status_str(self):
        return str(self.status)


jobs = {}


@app.route('/')
def base_route():
    return render_template('jobs.html', jobs=list(jobs.values()))

@app.route('/job', methods=['POST'])
def job_route():
    print(request.form)
    if request.method == 'POST':
        new_job = Job(request.form['gitUrl'])
        jobs[new_job.id] = new_job
        return redirect("/")
    if request.method == 'GET':
        return jsonify(list(jobs.values()))


@app.route('/job/pop', methods=['GET'])
def job_pop_route(id):
    if request.method == 'GET':
        pop_job = next(filter(lambda job: job.status == "QUEUED", jobs), None)
        if pop_job is not None:
            return jsonify(pop_job)
        else:
            return make_response('', 204)

@app.route('/job/<int:id>/start', methods=['PUT'])
def job_start_route(id):
    if request.method == 'PUT':
        if id in jobs:
            jobs[id].status = Status.RUNNING
            return make_response('', 200)
        else:
            return make_response('', 404)

@app.route('/job/<int:id>/results', methods=['GET', 'PUT'])
def job_results_route(id):
    if request.method == 'GET':
        if id in jobs:
            job = jobs[id]
            if job.status == Status.COMPLETE:
                return jsonify({"results": job.result})
            else:
                return make_response('', 204)
        else:
            return make_response('', 404)
    if request.method == 'PUT':
        if id in jobs:
            job = jobs[id]
            req_data = request.get_json()

            job.status = Status.COMPLETE
            job.results = req_data['results']
            return make_response('', 200)
        else:
            return make_response('', 404)