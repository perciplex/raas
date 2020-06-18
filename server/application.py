import uuid
import random
import sys
import queue
import datetime
import time
from flask import (
    Flask,
    jsonify,
    request,
    render_template,
    redirect,
    make_response,
)
from flask_sslify import SSLify


from hardware import Hardware
from json import JSONEncoder

rd = random.Random()
rd.seed(0)
application = Flask(__name__)
application.config.from_pyfile("config.cfg")

sslify = SSLify(application)


print(application.config["PI_IPS"])

# a status enum
class Status:
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"


# a class for queued, running, or completed jobs
class Job:
    def __init__(self, user, name, git_url):
        self.id = str(uuid.UUID(int=rd.getrandbits(128)))  # a random id
        self.name = name  # github project name
        self.user = user  # github user id
        self.git_url = git_url  # github hrl
        self.status = Status.QUEUED  # job status
        self.hardware = None  # the hardware the job is/was run on, none if queued
        self.stdout = "Results pending."  # job results
        self.data = (
            None  # observations, actions, reqards, and times for the job data points
        )
        self.queued_time = time.time()
        self.running_time = None
        self.completed_time = None

    def __hash__(
        self,
    ):  # define the hash function so that Job objects can be used in a set
        return hash(self.id)

    def __eq__(self, other):  # also so Job objects can be used in sets
        if isinstance(other, Job):
            return self.id == other.id
        else:
            return False

    def __dict__(self):  # a function for making the job serializable
        return {
            "id": self.id,
            "name": self.name,
            "user": self.user,
            "git_url": self.git_url,
            "stdout": self.stdout,
            "data": self.data,
            "status": self.status,
            "hardware": self.hardware,
            "queued_time": self.queued_time,
            "running_time": self.running_time,
            "completed_time": self.completed_time,
        }


# a custom json encoder which replaces the default and allows Job objects to be jsonified
class JSONEncoderJob(JSONEncoder):
    def default(self, job):
        try:
            if isinstance(
                job, Job
            ):  # if the object to be encoded is a job, use the dict() function
                return job.__dict__()
        except TypeError:
            pass
        return JSONEncoder.default(self, job)


# replace the default encoder
application.json_encoder = JSONEncoderJob


def format_datetime(value):
    return datetime.datetime.fromtimestamp(value).strftime("%m/%d/%y %H:%M:%S")


application.jinja_env.filters["datetime"] = format_datetime

# a dictionary of all jobs
# TODO: replace with a database


jobs = {}
queued = queue.Queue()  # a queue for the queued jobs
running = {}  # a set of running jobs
completed = queue.LifoQueue(maxsize=20)  # a queue of recently completed jobs

hardware_list = ["Omar", "Goose", "Nicki", "Beth"]
hardware_dict = {name: Hardware(name) for name in hardware_list}


def reset_jobs():
    global jobs, queued, running, completed
    jobs = {}

    queued = queue.Queue()  # a queue for the queued jobs
    running = {}  # a set of running jobs
    completed = queue.Queue(maxsize=20)  # a queue of recently completed jobs


def check_ip(ip):
    print(ip)
    return ip in application.config["PI_IPS"]


@application.route("/reset")
def reset_route():
    if not check_ip(request.remote_addr):
        print("reset request from non-pi ip")
        return make_response("", 403)
    reset_jobs()
    return redirect("/")


@application.route("/")
def base_route():
    # return send_file("static/index.html")
    return render_template("index.html")


@application.route("/status")
def status_route():
    return render_template("hardware.html")


@application.route("/hardware")
def hardware_route():
    return jsonify(
        sorted(
            [
                {
                    "name": hardware.name,
                    "status": "ONLINE" if hardware.is_alive() else "OFFLINE",
                }
                for hardware in hardware_dict.values()
            ],
            key=lambda hw: hw["name"],
        )
    )


@application.route("/job/<string:id>", methods=["GET"])
def job_page_route(id):
    if id in jobs:
        return render_template("job.html", job=jobs[id])
    else:
        return redirect("/")


@application.route("/submit", methods=["GET"])
def submit_page_route():
    return render_template("submit.html")


@application.route("/job", methods=["POST", "GET"])
def job_route():
    if request.method == "POST":
        user, name, git = (
            request.form["user"],
            request.form["name"],
            request.form["git"],
        )
        for job in queued.queue:
            if (user, name) == (job.user, job.name):
                return redirect("/")
        new_job = Job(user, name, git)
        jobs[new_job.id] = new_job  # add to database
        queued.put(new_job)  # add to queue
        return redirect("/")
    if request.method == "GET":
        return jsonify(
            {
                "queued": sorted(list(queued.queue), key=lambda job: -job.queued_time),
                "running": sorted(
                    list(running.values()), key=lambda job: -job.running_time
                ),
                "completed": sorted(
                    list(completed.queue), key=lambda job: -job.completed_time
                ),
            }
        )


@application.route("/job/pop", methods=["GET"])
def job_pop_route():
    if request.method == "GET":
        if not check_ip(request.remote_addr):
            print("pop request from non-pi ip")
            return make_response("", 403)

        req_hardware = request.args.get("hardware")
        print(req_hardware)
        if req_hardware in hardware_dict:
            hardware_dict[req_hardware].heartbeat()

        if not queued.empty():

            pop_job = queued.get()  # get job from queue
            # pop_job.hardware = (
            #    "Pendulum-1"
            # )  # set hardware of job TODO: actually set this to a meaningful value
            pop_job.hardware = req_hardware

            running[pop_job.id] = pop_job  # add to running dict
            pop_job.status = Status.RUNNING
            pop_job.running_time = time.time()
            # return jsonify({"git_url": pop_job.git_url, "id": pop_job.id})

            if req_hardware in hardware_dict:
                hardware_dict[req_hardware].starting_job()

            return jsonify(pop_job)
        else:
            return make_response("", 204)


@application.route("/job/<string:id>/results", methods=["PUT"])
def job_results_route(id):
    if request.method == "PUT":
        if not check_ip(request.remote_addr):
            print("results request from non-pi ip")
            return make_response("", 403)
        if id in jobs:
            job = jobs[id]  # look up job
            del running[id]  # remove from running dict

            completed.put(job)  # add to completed buffer

            req_data = request.get_json()

            job.stdout = req_data["stdout"]
            job.data = str(req_data["data"])

            if req_data["failed"]:
                job.status = Status.FAILED
            else:
                job.status = Status.COMPLETE

            print(job.data)
            job.completed_time = time.time()
            return make_response("", 200)
        else:
            return make_response("", 404)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "prod":
        application.run(port=80, host="0.0.0.0")
    else:
        application.run(debug=True)
