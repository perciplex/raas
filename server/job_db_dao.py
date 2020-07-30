#!/usr/bin/python

import datetime
import logging as log
import psycopg2
import psycopg2.extras
import os
from common import JOB_STATUS_LIST, JobStatus

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


def reconnect(func):
    """
    Wrapper fumctions to reconnect to DB if connection is dropped
    """

    def wrapper(db_conn, *args, **kwargs):
        if not db_conn.is_connected():
            log.info("Lost DB connection, reconnecting...")
            db_conn.connect_DB()

        return func(db_conn, *args, **kwargs)

    return wrapper


class JobDbDao:
    """
    Dao for the jobs table in raas-jobs database. Mmaintains and act on DB connection,
    add new jobs, updates jobs statuses, deletes jobs, and returns job lists by status.
    """

    def __init__(self):
        # Init logging from basicConfig
        log.basicConfig(level=log.INFO)

        # Establish DB connection
        self.conn = None
        self.connect_DB()

    def connect_DB(self):
        """
        Connect to the database using psycopg2 connect.
        """
        log.info("Establishing DB connection...")
        self.conn = psycopg2.connect(**DB_KWARGS)

    def is_connected(self):
        """
        Checks if the DB connection is alive
        """
        return self.conn and self.conn.closed == 0

    def disconnect_DB(self):
        """
        Disconnects from the database using close()
        """
        log.info("Closing DB connection...")
        self.conn.close()

    def reconnect_DB(self):
        if not self.db_conn.is_connected():
            log.info("Lost DB connection, reconnecting...")
            self.db_conn.connect_DB()

    @reconnect
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

        if status not in JOB_STATUS_LIST:
            log.error(
                "Invalid status provided! {} not in {}".format(status, JOB_STATUS_LIST)
            )
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

    @reconnect
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
            log.error("ERROR: {} rows found for ID {}!".format(len(job_rows), id))
            return None
        else:
            log.debug("Job not found for ID {}".format(id))
            return None

    @reconnect
    def insert_new_job(self, project_name, git_url, git_user):
        """
        Create the new row for the job in the jobs database.

        args:
            project_name (str):     Project name of the job
            git_url (str):          Git url for repo of the jobs
            git_user (int):         Git user of the job
        """

        log.info("Adding new job: {}, {}, {}".format(project_name, git_url, git_user))

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
                        JobStatus.QUEUED,
                        project_name,
                        git_url,
                        git_user,
                    ),
                )

    @reconnect
    def update_start_job(self, id, hardware_name):
        """
        Update the state of the job to RUNNING and update the start_time.
        Asserts the job is in QUEUD state before updating.

        args:
            id (str):               ID corresponding to the job to start
            hardware_name (str):    Name of hardware job is submitted to.
        """

        job = self.get_job_by_id(id)
        if job is None:
            log.warn("Job not found for ID {} ... Aborting job start.".format(id))
            return None

        if job["status"] != JobStatus.QUEUED:
            log.warn("Status must be QUEUED to start job, not {}".format(job["status"]))
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

    @reconnect
    def update_end_job(self, id, failed):
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
            log.warn("Job not found for ID {} ... Aborting job end.".format(id))
            return None

        if job["status"] != JobStatus.RUNNING:
            log.warn("Status must be RUNNING to end job, not {}".format(job["status"]))
            return None

        status = JobStatus.FAILED if failed else JobStatus.COMPLETED

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
        Deletes a job from the jobs table.

        args:
            id (str):           ID corresponding to the job to end
            failed (bool):      Boolean for if the job failed
        """

        job = self.get_job_by_id(id)

        if not job:
            log.warn("Job not found for ID {} ... Aborting delete.".format(id))
            return None

        with self.conn:
            with self.conn.cursor() as curs:
                curs.execute(
                    """
                    DELETE FROM jobs
                    WHERE id = %s;
                    """,
                    (id,),
                )
            log.info("Deleted job {} from database.".format(id))


if __name__ == "__main__":
    # For testing, not meant to be run as a standalone.
    job_dao = JobDbDao()

    # Get all jobs
    for status in JOB_STATUS_LIST:
        jobs = job_dao.get_jobs_by_status(status, limit=20)
        print("\n{} JOBS ({})".format(status, len(jobs)))
        for j in jobs:
            print(j)
