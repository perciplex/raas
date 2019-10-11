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
    def __init__(self, user, name, git):
        self.id = uuid.uuid1()
        self.name = name
        self.user = user
        self.git = git
        self.status = Status.QUEUED
        self.results = "Results pending."
    def __dict__(self):
        return {"id": self.id, "gitUrl":self.git, "results":self.results, "status":self.status}
    def status_str(self):
        return str(self.status)

jobs = {}
new_job = Job("testUser", "testName", f"testUrl")
jobs[str(new_job.id)] = new_job

print(jobs)

@app.route('/')
def base_route():
    #return send_file("static/index.html")
    return render_template('index.html', jobs=list(jobs.values()))

@app.route('/job', methods=['GET', 'POST'])
def job_route():
    print(request.form)
    if request.method == 'POST':
        print(request.form)
        new_job = Job(request.form['user'], request.form['name'],request.form['git'])
        jobs[str(new_job.id)] = new_job
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

@app.route('/job/<string:id>', methods=['GET'])
def job_page_route(id):
    return render_template('job.html', job=jobs[id])

    
@app.route('/submit', methods=['GET'])
def submit_page_route():
    return render_template('submit.html')

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