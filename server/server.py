from flask import Flask, jsonify, request, render_template, redirect, make_response, send_file
app = Flask(__name__)
from collections import namedtuple
from enum import Enum
import uuid
import sys


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
        return {"id": self.id, "gitUrl":self.git, "results":self.results, "status":self.status}
    def status_str(self):
        return str(self.status)


jobs = {0:Job("testUrl")}


@app.route('/')
def base_route():
    return send_file("static/index.html")
    #return render_template('jobs.html', jobs=list(jobs.values()))

@app.route('/job', methods=['GET', 'POST'])
def job_route():
    print(request.form)
    if request.method == 'POST':
        new_job = Job(request.form['gitUrl'])
        jobs[new_job.id] = new_job
        return redirect("/")
    if request.method == 'GET':
        return jsonify([job.__dict__() for job in list(jobs.values())])


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

if __name__ == "__main__":
    app.run(port=sys.argv[1], debug=True)