from flask import (
    Flask,
    jsonify,
    request,
    render_template,
    redirect,
    make_response,
    send_file,
)

app = Flask(__name__)
from enum import Enum
import uuid
import random

rd = random.Random()
rd.seed(0)
import sys
import queue


app = Flask(__name__)


class Status:
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    COMPLETE = "COMPLETE"


class Job:
    def __init__(self, user, name, git):
        # self.id = str(uuid.uuid4())

        self.id = str(uuid.UUID(int=rd.getrandbits(128)))
        print(self.id)
        self.name = name
        self.user = user
        self.git = git
        self.status = Status.QUEUED
        self.hardware = None
        self.results = "Results pending."

    def __dict__(self):
        return {
            "id": self.id,
            "gitUrl": self.git,
            "results": self.results,
            "status": self.status,
        }

    def status_str(self):
        return str(self.status)


jobs = {}

queued = queue.Queue()
running = {}
completed = queue.Queue()

for i in range(1):
    new_job = Job("Perciplex", "hello world", f"https://github.com/perciplex/raas-starter.git")
    jobs[new_job.id] = new_job
    queued.put(new_job)

new_job = Job("kimbers2007", "rl_controller", f"testUrl2")
jobs[new_job.id] = new_job
new_job.status = Status.RUNNING
new_job.hardware = "Pendulum-1"
running[new_job.id] = new_job

new_job = Job("lizzyB", "liz-controller", f"testUrl3")
jobs[new_job.id] = new_job
new_job.status = Status.COMPLETE
new_job.hardware = "Pendulum-1"
new_job.results = """
[-0.02180978  0.03024429  0.00471958 -0.01161285]
[-0.0212049  -0.16494503  0.00448732  0.28255542]
[-0.0245038  -0.3601307   0.01013843  0.57665024]
[-0.03170641 -0.55539328  0.02167144  0.87250971]
[-0.04281428 -0.36057263  0.03912163  0.58671826]
[-0.05002573 -0.16601981  0.050856    0.30661115]
[-0.05334613 -0.36182817  0.05698822  0.61488917]
[-0.06058269 -0.55769814  0.069286    0.92496264]
[-0.07173665 -0.75368406  0.08778526  1.23858996]
[-0.08681033 -0.94981699  0.11255706  1.55743223]
[-0.10580667 -1.1460926   0.1437057   1.88300458]
[-0.12872853 -1.34245716  0.18136579  2.21661946]
"""
completed.put(new_job)


print(completed.queue)


@app.route("/")
def base_route():
    # return send_file("static/index.html")
    return render_template(
        "index.html",
        queued=list(queued.queue),
        running=list(running.values()),
        completed=list(completed.queue),
    )


@app.route("/job/<string:id>", methods=["GET"])
def job_page_route(id):
    return render_template("job.html", job=jobs[id])


@app.route("/submit", methods=["GET"])
def submit_page_route():
    return render_template("submit.html")


@app.route("/job", methods=["POST"])
def job_route():
    print(request.form)
    if request.method == "POST":
        print(request.form)
        new_job = Job(request.form["user"], request.form["name"], request.form["git"])

        jobs[new_job.id] = new_job  # add to database
        queued.put(new_job)  # add to queue

        return redirect("/")


@app.route("/job/pop", methods=["GET"])
def job_pop_route():
    if request.method == "GET":
        if not queued.empty():

            pop_job = queued.get()  # get job from queue
            pop_job.hardware = (
                "Pendulum-1"
            )  # set hardware of job TODO: actually set this to a meaningful value

            running[pop_job.id] = pop_job  # add to running dict
            pop_job.status = Status.RUNNING
            return jsonify({
                "git_url": pop_job.git,
                "id": pop_job.id
                })
        else:
            return make_response("", 204)


@app.route("/job/<string:id>/results", methods=["PUT"])
def job_results_route(id):
    if request.method == "PUT":
        if id in jobs:
            job = jobs[id]  # look up job
            del running[id]  # remove from running dict

            completed.put(job)  # add to completed buffer

            req_data = request.get_json()

            job.status = Status.COMPLETE
            job.results = req_data["results"]
            return make_response("", 200)
        else:
            return make_response("", 404)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "prod":
        app.run(port=80, host="0.0.0.0")
    else:
        app.run(debug=True)
