from flask import Flask, jsonify, request, render_template, redirect
app = Flask(__name__)
from collections import namedtuple
from enum import Enum


class Status():
    PENDING = 'PENDING'
    RUNNING = 'RUNNING'
    COMPLETE = 'COMPLETE'

class Job:
    id_counter = 0
    def __init__(self, git):
        self.id = Job.id_counter
        Job.id_counter += 1
        self.git = git
        self.status = Status.PENDING
        self.results = "Results pending."
    def __dict__(self):
        return {"id": self.id, "results":self.results, "status":self.status}
    def status_str(self):
        return str(self.status)


jobs = {}


@app.route('/jobs', methods=['GET','POST'])
def jobs_route():
    print(request.form)
    if request.method == 'POST':
        new_job = Job(request.form['git'])
        jobs[new_job.id] = new_job
        return redirect("/")
    if request.method == 'GET':
        pending_jobs = list(filter(lambda job: job.status==Status.PENDING, jobs.values()))
        if len(pending_jobs) == 0:
            return jsonify(success=True)
        return jsonify(pending_jobs[0])


@app.route('/')
def base_route():
    return render_template('jobs.html', jobs=list(jobs.values()))

@app.route('/status/<int:id>', methods=['GET','POST'])
def status_route(id):
    if request.method == 'POST':
        req_data = request.get_json()
        status = req_data['status']
        if status == "RUNNING":
            jobs[id].status = Status.RUNNING
        elif status == "COMPLETE":
            jobs[id].status = Status.COMPLETE
        else:
            return jsonify(success=False)
        return jsonify(success=True)
    if request.method == 'GET':
        return jsonify(jobs[id].status)


@app.route('/results/<int:id>', methods=['GET','POST'])
def results_route(id):
    if request.method == 'POST':
        req_data = request.get_json()
        jobs[id].status = Status.COMPLETE
        jobs[id].results = req_data['results']
        return jsonify(success=True)
    if request.method == 'GET':
        return jsonify(jobs[id].results)