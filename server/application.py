import random
import sys
import time
import uuid
import logging as log
from collections import deque
from json import JSONEncoder
from common import JobStatus
from hardware import Hardware

from job_db_dao import JobDbDao
from flask import Flask, jsonify, make_response, redirect, request


rd = random.Random()
rd.seed(0)
application = Flask(__name__, static_folder="raas-frontend/build", static_url_path="/")
application.config.from_pyfile("config.cfg")

# sslify = SSLify(application)


class Job:
    """
    Class for queued, running, or completed jobs
    """

    def __init__(self, git_user, project_name, git_url):
        self.id = str(uuid.UUID(int=rd.getrandbits(128)))  # a random id
        self.project_name = project_name  # github project name
        self.git_user = git_user  # github user id
        self.git_url = git_url  # github hrl
        self.status = JobStatus.QUEUED  # job status
        self.hardware_name = None  # the hardware the job is/was run on, none if queued
        self.stdout = "Results pending."  # job results
        # observations, actions, reqards, and times for the job data points
        self.data = None
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


class JobsCache:
    """
    A class that holds the most recent cached results, so the frontend won't
    ping the database for each page load.

    args:
       job_dao (JobDbDao):  Job DB Dao class object for jobs DB
    """

    def __init__(self, job_dao):
        self.job_db_dao = job_dao
        self.last_db_read_time = time.time()
        self.update_period_seconds = 1.0  # In seconds
        self.cache = {
            "queued": deque(),
            "running": {},
            "completed": {},
            "all_jobs": {},
        }
        self.update_db_cache()  # update to begin

    def get_db_cache(self):
        """
        Get the database cache if the update period has passed since last pull
        """
        if time.time() - self.last_db_read_time > self.update_period_seconds:
            self.update_db_cache()
        return self.cache

    def update_db_cache(self):
        """
        Update the database cache. Get all queued, running, and completed jobs.
        Convert queued jobs to a deque.
        """

        def list_to_dict(row_list):
            if row_list:
                return {row["id"]: row for row in row_list}
            else:
                return {}

        self.last_db_read_time = time.time()
        q = list_to_dict(self.job_db_dao.get_jobs_by_status(JobStatus.QUEUED))
        r = list_to_dict(self.job_db_dao.get_jobs_by_status(JobStatus.RUNNING))
        c = list_to_dict(
            self.job_db_dao.get_jobs_by_status(JobStatus.COMPLETED, sort_order="DESC")
        )
        f = list_to_dict(
            self.job_db_dao.get_jobs_by_status(JobStatus.FAILED, sort_order="DESC")
        )

        self.cache = {
            "queued": deque(q.values()),
            "running": r,
            "completed": {**c, **f},
            "all_jobs": {**q, **r, **c, **f},
        }

    def get_job_in_cache_from_id(self, id, cache="all_jobs"):
        """
        Gets the job if it exists in the cache.

        Args:
            id (UUID): ID of the job.
            cache (str): Which cache to check. Defaults to "all_jobs".

        Returns:
            job (dict)
        """
        if self.check_job_in_cache_from_id(id, cache=cache):
            return self.cache[cache][id]
        else:
            return None

    def check_job_in_cache_from_id(self, id, cache="all_jobs"):
        """
        Checks if the job id exists in the cache.

        Args:
            id (UUID): ID of the job.
            cache (str): Which cache to check. Defaults to "all_jobs".

        Returns:
            bool
        """
        return id in self.cache[cache]


class JSONEncoderJob(JSONEncoder):
    """
    Custom json encoder which jsonifies Job objects. Inherits JSONEncoder
    """

    def default(self, job):
        try:
            # if the object to be encoded is a job, use the dict() function
            if isinstance(job, Job):
                return job.__dict__()

        except TypeError:
            pass
        return JSONEncoder.default(self, job)


def check_password(password):
    """
    Checks that the request has required password.

    args:
        password (str): Password supplied by request.
    returns:
        bool:           If password matches flask config
    """
    if password == application.config["FLASK_PASS"]:
        log.error(
            "Bad password from from host: {}".format(request.args.get("hardware"))
        )
        return False
    else:
        return True


@application.route("/")
def index():
    return application.send_static_file("index.html")


@application.route("/api/hardware")
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


@application.route("/api/job/<string:id>", methods=["GET"])
def job_page_route(id):
    jobs_cache.get_db_cache()
    job = jobs_cache.get_job_in_cache_from_id(id, "all_jobs")
    if job:
        return jsonify(job)
    else:
        return redirect("/")


@application.route("/api/job", methods=["POST", "GET"])
def job_route():
    jobs_cache.get_db_cache()
    if request.method == "POST":
        log.info("New job: {}".format(request))
        git_user, project_name, git_url = (
            request.form["git_user"],
            request.form["project_name"],
            request.form["git_url"],
        )

        # If git project already in queued cache, dont create job.
        for job in jobs_cache.cache["queued"]:
            if (git_user, project_name) == (job["git_user"], job["project_name"],):
                log.info("Job already in queued. Skipping creation.")
                return redirect("/")

        # Else, add new job
        job_db_dao.insert_new_job(project_name, git_url, git_user)
        return redirect("/")

    # Need to update with DB stuff
    if request.method == "GET":
        return jsonify(
            {
                "queued": (list(jobs_cache.cache["queued"])),
                "running": (list(jobs_cache.cache["running"].values())),
                "completed": (list(jobs_cache.cache["completed"].values())),
            }
        )


@application.route("/api/job/pop", methods=["GET"])
def job_pop_route():
    jobs_cache.get_db_cache()
    if request.method == "GET":
        if not check_password(request.args["FLASK_PASS"]):
            return make_response("Bad password.", 403)

        req_hardware = request.args.get("hardware")
        if req_hardware not in hardware_dict:
            log.error("Hardware {} not found in hardware_dict".format(req_hardware))
            return make_response("Hardware not found in hardware_dict", 500)

        hardware_dict[req_hardware].heartbeat()

        # If there are queued jobs, pop one, update the db row, and return the job
        if jobs_cache.cache["queued"]:
            hardware_dict[req_hardware].starting_job()

            pop_job = jobs_cache.cache["queued"].pop()  # get job from queue
            job_db_dao.update_start_job(pop_job["id"], req_hardware)

            log.info("{} has popped job {}.".format(req_hardware, pop_job["id"]))
            return jsonify(pop_job)
        else:
            return make_response("", 204)


@application.route("/api/job/<string:id>/results", methods=["PUT"])
def job_results_route(id):
    req_hardware = request.args.get("hardware")
    if request.method == "PUT":
        status = request.json["failed"]
        if not check_password(request.args["FLASK_PASS"]):
            return make_response("", 403)

        job_db_dao.update_end_job(id, status)
        log.info("{} has completed job {}.".format(req_hardware, id))
        return make_response("", 200)


hardware_list = ["Omar", "Goose", "Nicki", "Beth"]
hardware_dict = {name: Hardware(name) for name in hardware_list}

job_db_dao = JobDbDao()
jobs_cache = JobsCache(job_db_dao)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "prod":
        application.run(port=80, host="0.0.0.0")
    else:
        application.run(debug=True)
