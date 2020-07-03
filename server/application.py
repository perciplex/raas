import uuid
import random
import sys
import queue
from collections import deque
import datetime
import time, json
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

import database_fns

rd = random.Random()
rd.seed(0)
application = Flask(__name__)
application.config.from_pyfile("config.cfg")

# sslify = SSLify(application)

# a status enum
class Status:
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"


# a class for queued, running, or completed jobs
class Job:
    def __init__(self, git_user, project_name, git_url):
        self.id = str(uuid.UUID(int=rd.getrandbits(128)))  # a random id
        self.project_name = project_name  # github project name
        self.git_user = git_user  # github user id
        self.git_url = git_url  # github hrl
        self.status = Status.QUEUED  # job status
        self.hardware_name = None  # the hardware the job is/was run on, none if queued
        self.stdout = "Results pending."  # job results
        self.data = (
            None  # observations, actions, reqards, and times for the job data points
        )
        self.submit_time = time.time()
        self.start_time = None
        self.end_time = None

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
            "project_name": self.project_name,
            "git_user": self.git_user,
            "git_url": self.git_url,
            "stdout": self.stdout,
            "data": self.data,
            "status": self.status,
            "hardware_name": self.hardware_name,
            "submit_time": self.submit_time,
            "start_time": self.start_time,
            "end_time": self.end_time,
        }


# A class that holds the most recent cached results, so the frontend won't
# ping the database for each page load.
class JobsCache:
    def __init__(self):

        self.last_db_read_time = time.time()
        self.update_period = 2.0  # In seconds
        self.cache = {
            "queued": deque(),
            "running": {},
            "completed": {},
            "all_jobs": {},
        }
        self.update_db_cache()  # update to begin

    def get_db_cache(self):

        if time.time() - self.last_db_read_time > self.update_period:
            self.update_db_cache()
        return self.cache

    def update_db_cache(self):
        q = database_fns.get_all_queued()
        r = database_fns.get_all_running()
        c = database_fns.get_all_completed()

        self.cache = {
            "queued": deque(q),
            "running": r,
            "completed": c,
            "all_jobs": q + r + c,
        }

    def get_job_id_in_cache(self, id, cache="all_jobs"):
        return next((job for job in self.cache[cache] if job["id"] == str(id)), None,)

    def check_job_id_in_cache(self, id, cache="all_jobs"):
        return (
            next((item for item in self.cache[cache] if item["id"] == str(id)), None,)
        ) is not None


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


jobs = {}
queued = queue.Queue()  # a queue for the queued jobs
running = {}  # a set of running jobs
completed = queue.LifoQueue(maxsize=20)  # a queue of recently completed jobs

hardware_list = ["Omar", "Goose", "Nicki", "Beth"]
hardware_dict = {name: Hardware(name) for name in hardware_list}
jobs_cache = JobsCache()


def reset_jobs():
    global jobs, queued, running, completed
    jobs = {}

    queued = queue.Queue()  # a queue for the queued jobs
    running = {}  # a set of running jobs
    completed = queue.Queue(maxsize=20)  # a queue of recently completed jobs


def check_password(password):
    if password == application.config["FLASK_PASS"]:
        print("Bad password from from host")
        return False
    else:
        return True


@application.route("/reset")
def reset_route():
    pop_job = jobs_cache.cache["queued"].pop()  # get job from queue
    print(jsonify(pop_job))
    if not check_password(request.args["FLASK_PASS"]):
        return make_response("", 403)
    reset_jobs()
    return redirect("/")


@application.route("/")
def base_route():
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
    jobs_cache.get_db_cache()
    print("Looking for {} in {}\n\n\n".format(id, jobs_cache.cache["all_jobs"]))
    job = jobs_cache.get_job_id_in_cache(id, "all_jobs")
    if job:
        print("\n\nCACHE HIT: \n {} \n\n".format(job))
        return render_template("job.html", job=job)
    else:
        return redirect("/")


@application.route("/submit", methods=["GET"])
def submit_page_route():
    return render_template("submit.html")


@application.route("/job", methods=["POST", "GET"])
def job_route():
    jobs_cache.get_db_cache()
    if request.method == "POST":
        git_user, project_name, git_url = (
            request.form["git_user"],
            request.form["project_name"],
            request.form["git_url"],
        )

        for job in jobs_cache.cache["queued"]:
            if (git_user, project_name) == (job["git_user"], job["project_name"]):
                return redirect("/")

        # Else, add new job
        database_fns.new_job(project_name, git_url, git_user)

        return redirect("/")
    # Need to update with DB stuff
    if request.method == "GET":
        return jsonify(
            {
                "queued": (list(jobs_cache.cache["queued"])),
                "running": (list(jobs_cache.cache["running"])),
                "completed": (list(jobs_cache.cache["completed"])),
            }
        )


@application.route("/job/pop", methods=["GET"])
def job_pop_route():
    jobs_cache.get_db_cache()
    if request.method == "GET":
        if not check_password(request.args["FLASK_PASS"]):
            return make_response("Bad password.", 403)

        req_hardware = request.args.get("hardware")
        print(req_hardware)
        if req_hardware in hardware_dict:
            hardware_dict[req_hardware].heartbeat()

        if jobs_cache.cache["queued"]:

            # job_id = database_fns.get_next_queued()

            pop_job = jobs_cache.cache["queued"].pop()  # get job from queue
            database_fns.start_job(pop_job["id"], req_hardware)

            if req_hardware in hardware_dict:
                hardware_dict[req_hardware].starting_job()

            return jsonify(pop_job)
        else:
            return make_response("", 204)


@application.route("/job/<string:id>/results", methods=["PUT"])
def job_results_route(id):
    jobs_cache.get_db_cache()
    if request.method == "PUT":
        if not check_password(request.args["FLASK_PASS"]):
            return make_response("", 403)
        if jobs_cache.check_job_id_in_cache(id):

            database_fns.end_job(id)

            # job = jobs[id]  # look up job
            # del running[id]  # remove from running dict

            # completed.put(job)  # add to completed buffer

            # req_data = request.get_json()

            return make_response("", 200)
        else:
            return make_response("", 404)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "prod":
        application.run(port=80, host="0.0.0.0")
    else:
        application.run(debug=True)
