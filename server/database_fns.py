#!/usr/bin/python

import datetime
import logging
import psycopg2
import psycopg2.extras
import os

JOBS_DB = os.getenv("JOBS_DB", None)
JOBS_DB_USER = os.getenv("JOBS_DB_USER", None)
JOBS_DB_PASS = os.getenv("JOBS_DB_PASS", None)
JOBS_DB_HOST = os.getenv("JOBS_DB_HOST", None)
JOBS_DB_PORT = os.getenv("JOBS_DB_PORT", None)


DB_KWARGS = {
    "database": JOBS_DB,
    "user": JOBS_DB_USER,
    "password": JOBS_DB_PASS,
    "host": JOBS_DB_HOST,
    "port": JOBS_DB_PORT,
}

VALID_STATUSES = ["QUEUED", "RUNNING", "COMPLETED", "FAILED"]
JOB_STATUSES = {
    "QUEUED": "QUEUED",
    "RUNNING": "RUNNING",
    "COMPLETED": "COMPLETED",
    "FAILED": "FAILED",
}


class Job_DB_Connection:
    """
    Class to maintain and act on DB connection.
    """

    def __init__(self):
        # Init logging from basicConfig
        logging.basicConfig(level=logging.DEBUG)

        # Establish DB connection
        logging.info("Establishing DB connection...")
        self.conn = psycopg2.connect(**DB_KWARGS)

    def __del__(self):
        self.conn.close()

    def get_jobs_by_status(self, status, sort_order="ASC", limit=20):
        """
        Get all jobs of one type from the DB, sorted by earliest submit_time.
        Returns them as a list of dicts.

        args:
            status (str):       Status of jobs to get. Should be in VALID_STATUSES enum
            sort_order (str):   Sort order of query. Defaults to "ASC" (ascending).
            limit (int):        Maximum number of jobs to return
        returns:
            jobs (list):        A list of dictionaries for each job matching status
        """

        def _real_dicts_to_python_dicts(real_dict_list):
            """
            Convert the postgres psycopg2 RealDictRows to python dict.
            """
            real_dict_list = [dict(row) for row in real_dict_list]
            return real_dict_list

        if status not in VALID_STATUSES:
            logging.info("Must provide a valid status! Provided {}".format(status))
            return None

        with self.conn:
            with self.conn.cursor(
                cursor_factory=psycopg2.extras.RealDictCursor
            ) as curs:
                curs.execute(
                    """
                    SELECT * FROM jobs
                    WHERE status = %s
                    LIMIT %s;
                    """,
                    (status, limit),
                )
                rows = curs.fetchall()

        return _real_dicts_to_python_dicts(rows)

    def get_job_by_id(self, id):
        """
        Get the job row corresponding of provided job id.
        Asserts there is only 1 job matching ID.

        args:
            id (str):           ID corresponding to the job to start
        returns:
            job (RealDictRow):  A RealDictRows representation of the job
        """
        with self.conn:
            with self.conn.cursor(
                cursor_factory=psycopg2.extras.RealDictCursor
            ) as curs:
                curs.execute(
                    """
                    SELECT * FROM jobs
                    WHERE id = %s;
                    """,
                    (id,),
                )
                job_rows = curs.fetchall()

        if len(job_rows) == 1:
            return job_rows[0]
        if len(job_rows) > 1:
            logging.error("ERROR: {} rows found for ID {}!".format(len(job_rows), id))
            return None
        else:
            logging.info("Job not found for ID {}".format(id))
            return None

    def new_job(self, project_name, git_url, git_user):
        """
        Create the new row for the job in the jobs database.

        args:
            project_name (str):     Project name of the job
            git_url (str):          Git url for repo of the jobs
            git_user (int):         Git user of the job
        """

        logging.info("Adding new job: ", project_name, git_url, git_user)

        with self.conn:
            with self.conn.cursor() as curs:
                curs.execute(
                    """
                    INSERT INTO jobs
                    (submit_time, status, project_name, git_url, git_user)
                    VALUES(%s, %s, %s, %s, %s) RETURNING id;
                    """,
                    (
                        datetime.datetime.now(),
                        "QUEUED",
                        project_name,
                        git_url,
                        git_user,
                    ),
                )

    def start_job(self, id, hardware_name):
        """
        Update the state of the job to RUNNING and update the start_time.
        Asserts the job is in QUEUD state before updating.

        args:
            id (str):               ID corresponding to the job to start
            hardware_name (str):    Name of hardware job is submitted to.
        """

        job = self.get_job_by_id(id)
        if job is None:
            logging.info("Aborting job start ... job not found for ID {}".format(id))
            return None

        if job["status"] != "QUEUED":
            logging.info(
                "Status must be QUEUED to start job, not {}".format(job["status"])
            )
            return None

        with self.conn:
            with self.conn.cursor() as curs:
                curs.execute(
                    """
                    UPDATE jobs
                    SET status = 'RUNNING', hardware_name = %s, start_time = %s
                    WHERE id = %s;
                    """,
                    (hardware_name, datetime.datetime.now(), id),
                )

    def end_job(self, id, failed):
        """
        Update the state of the job to COMPLETE/FAILED based on the failed bool
        and update the end_time.
        Asserts the job is in RUNNING state before updating.

        args:
            id (str):           ID corresponding to the job to end
            failed (bool):      Boolean for if the job failed
        """

        job = self.get_job_by_id(id)

        if job is None:
            logging.info("Aborting job end ... job not found for ID {}".format(id))
            return None

        if job["status"] != "RUNNING":
            logging.info(
                "Status must be RUNNING to end job, not {}".format(job["status"])
            )
            return None

        status = "FAILED" if failed else "COMPLETED"

        with self.conn:
            with self.conn.cursor() as curs:
                curs.execute(
                    """
                    UPDATE jobs
                    SET status = %s, end_time = %s
                    WHERE id = %s;
                    """,
                    (status, datetime.datetime.now(), id),
                )

    def delete_job(self, id):
        """
        Update the state of the job to COMPLETE/FAILED based on the failed bool
        and update the end_time.
        Asserts the job is in RUNNING state before updating.

        args:
            id (str):           ID corresponding to the job to end
            failed (bool):      Boolean for if the job failed
        """

        job = self.get_job_by_id(id)

        if not job:
            logging.info("Job not found with ID {}... skipping delete.".format(id))

        with self.conn:
            with self.conn.cursor() as curs:
                curs.execute(
                    """
                    DELETE FROM jobs
                    WHERE id = %s;
                    """,
                    (id,),
                )
            logging.info("Deleted job {} from database.".format(id))


if __name__ == "__main__":
    # For testing it; not usually meant to be run as a standalone.
    db_conn = Job_DB_Connection()
    debug_id = "e6c8de9f-ebcc-451f-a109-341fd8f8b447"
    print(db_conn.get_job_by_id(debug_id))
    db_conn.start_job(debug_id, "GOOSE")
    db_conn.end_job(debug_id, True)
    db_conn.delete_job(debug_id)

    for status in JOB_STATUSES.values():
        jobs = db_conn.get_jobs_by_status(status, limit=100)
        print("\n{} JOBS ({})".format(status, len(jobs)))
        for j in jobs:
            print(j)
