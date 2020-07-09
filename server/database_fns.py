#!/usr/bin/python

import datetime

import psycopg2
import psycopg2.extras

DB_KWARGS = {
    "database": "postgres",
    "user": "perciplex",
    "password": "TVaH5aKw3iEAenP",
    "host": "raas-jobs.c0cgyyikkgwi.us-east-2.rds.amazonaws.com",
    "port": "5432",
}

VALID_STATUSES = ["QUEUED", "RUNNING", "COMPLETED", "FAILED"]


def real_dicts_to_python_dicts(real_dict_list):
    """
    Convert the postgres psycopg2 RealDictRows to python dict.

    args:
        real_dict_list (list): The psycopg2 RealDictRow list.

    """
    real_dict_list = [dict(row) for row in real_dict_list]
    return real_dict_list


def get_all_jobs_by_status(status):
    """

    Get all jobs of one type from the DB, sorted by earliest submit_time.
    Returns them as a list of dicts.

    """

    assert (
        status in VALID_STATUSES
    ), f"Must provide a valid status! Provided = {status}"

    # For COMPLETED, only want the most recent
    status_sort_order = {
        "QUEUED": "ASC",
        "RUNNING": "ASC",
        "COMPLETED": "DESC",
        "FAILED": "DESC",
    }

    n_lim = 20  # The number of jobs to get
    command = """
                SELECT
                    *
                FROM
                    jobs
                WHERE
                    status = '{}'
                ORDER BY
                    submit_time {}
                LIMIT {};
                """.format(
        status, status_sort_order[status], n_lim
    )

    conn = None
    try:

        conn = psycopg2.connect(**DB_KWARGS)  # Connect to DB
        cur = conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        )  # Get cursor
        cur.execute(command)  # Send the command

        # Returns just the top one. If there are no jobs, this
        # value should be None.
        rows = cur.fetchall()

        cur.close()  # close communication with the PostgreSQL database server
        conn.commit()  # commit the changes

        return real_dicts_to_python_dicts(rows)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def get_id_rows(id):

    """

    Get the rows corresponding to id.

    There should be only 1, but you can use this to check that the id is
    valid.

    Note: uses different cursor, so it can return a dict for each row.

    """

    command = """
                SELECT
                    *
                FROM
                    jobs
                WHERE
                    id = %s;
                """

    conn = None
    try:

        conn = psycopg2.connect(**DB_KWARGS)  # Connect to DB
        cur = conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        )  # Get cursor
        cur.execute(command, (id,))  # Send the command
        # Returns just the top one. If there is no queued, this
        # value should be None.
        rows = cur.fetchall()

        cur.close()  # close communication with the PostgreSQL database server
        conn.commit()  # commit the changes

        return rows

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


#  High level job control


def new_job(project_name, git_url, git_user):
    """

    Enter a new queued job into the DB.

    """
    print("Adding new job: ", project_name, git_url, git_user)
    command = """
            INSERT INTO jobs(submit_time, status, project_name, git_url, git_user)
            VALUES(%s, %s, %s, %s, %s) RETURNING id;
            """

    conn = None
    try:

        conn = psycopg2.connect(**DB_KWARGS)  # Connect to DB
        cur = conn.cursor()  # Get cursor
        cur.execute(
            command,
            (
                datetime.datetime.now(),
                "QUEUED",
                project_name,
                git_url,
                git_user,
            ),
        )  # Send the command

        cur.close()  # close communication with the PostgreSQL database server
        conn.commit()  # commit the changes

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def start_job(id, hardware_name):

    """

    Start a job. Must supply the unique id. Can get this for the next
    queued job with get_next_queued().

    """

    id_rows = get_id_rows(id)

    assert len(id_rows) == 1, "Invalid len(id_rows): {}".format(id_rows)

    job_row = id_rows[0]

    assert (
        job_row["status"] == "QUEUED"
    ), "Status must be queued to start job, is currently: {}".format(
        job_row["status"]
    )

    command = """
                UPDATE jobs
                SET
                    status = 'RUNNING',
                    hardware_name = %s,
                    start_time = %s
                WHERE id = %s;
                """

    conn = None
    try:

        conn = psycopg2.connect(**DB_KWARGS)  # Connect to DB
        cur = conn.cursor()  # Get cursor
        cur.execute(
            command, (hardware_name, datetime.datetime.now(), id)
        )  # Send the command

        cur.close()  # close communication with the PostgreSQL database server
        conn.commit()  # commit the changes

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def end_job(id):

    """

    End a job. Must supply the unique id.

    """

    id_rows = get_id_rows(id)

    assert len(id_rows) == 1, "Invalid len(id_rows): {}".format(id_rows)

    job_row = id_rows[0]

    assert (
        job_row["status"] == "RUNNING"
    ), "Status must be running to end job, is currently: {}".format(
        job_row["status"]
    )

    command = """
                UPDATE jobs
                SET
                    status = 'COMPLETED',
                    end_time = %s
                WHERE id = %s;
                """

    conn = None
    try:

        conn = psycopg2.connect(**DB_KWARGS)  # Connect to DB
        cur = conn.cursor()  # Get cursor
        cur.execute(command, (datetime.datetime.now(), id))  # Send the command

        cur.close()  # close communication with the PostgreSQL database server
        conn.commit()  # commit the changes

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    # For testing it; not usually meant to be run as a standalone.

    print(get_all_jobs_by_status("QUEUED"))
    print(get_all_jobs_by_status("RUNNING"))
    print(get_all_jobs_by_status("COMPLETED"))
