#!/usr/bin/python

import psycopg2
import psycopg2.extras
import datetime


DB_KWARGS = {
    "database": "postgres",
    "user": "perciplex",
    "password": "TVaH5aKw3iEAenP",
    "host": "raas-jobs.c0cgyyikkgwi.us-east-2.rds.amazonaws.com",
    "port": "5432",
}


def datetime_objs_to_strs(jobs):

    times = ["submit_time", "start_time", "end_time"]

    for j in jobs:
        for t in times:
            if j[t] is not None:
                # pass
                j[t] = j[t].strftime("%m/%d/%Y, %H:%M:%S")

    return jobs


def real_dicts_to_python_dicts(real_dict_list):
    """
    Convert the postgres psycopg2 RealDictRows to python dict.

    args:
        real_dict_list (list): The psycopg2 RealDictRow list.

    """
    real_dict_list = [dict(row) for row in real_dict_list]
    return real_dict_list


def get_all_queued():
    """

    Get all queued jobs from the DB, sorted by
    earliest submit_time. Returns them as a list of dicts.

    """

    command = """
                SELECT
                	*
                FROM
                	jobs
                WHERE
                    status = 'QUEUED'
                ORDER BY
                	submit_time ASC;
                """

    conn = None
    try:

        conn = psycopg2.connect(**DB_KWARGS)  # Connect to DB
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)  # Get cursor
        cur.execute(command)  # Send the command

        # Returns just the top one. If there is no queued, this
        # value should be None.
        rows = cur.fetchall()

        cur.close()  # close communication with the PostgreSQL database server
        conn.commit()  # commit the changes

        return real_dicts_to_python_dicts(datetime_objs_to_strs(rows))

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def get_all_running():
    """

    Get all running jobs from the DB, sorted by
    earliest submit_time. Returns them as a list of dicts.

    """

    command = """
                SELECT
                	*
                FROM
                	jobs
                WHERE
                    status = 'RUNNING'
                ORDER BY
                	start_time ASC;
                """

    conn = None
    try:

        conn = psycopg2.connect(**DB_KWARGS)  # Connect to DB
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)  # Get cursor
        cur.execute(command)  # Send the command

        # Returns just the top one. If there is no queued, this
        # value should be None.
        rows = cur.fetchall()

        cur.close()  # close communication with the PostgreSQL database server
        conn.commit()  # commit the changes

        return real_dicts_to_python_dicts(datetime_objs_to_strs(rows))

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def get_all_completed():
    """

    Get all completed jobs from the DB, sorted by
    earliest submit_time. Returns them as a list of dicts.

    """

    command = """
                SELECT
                	*
                FROM
                	jobs
                WHERE
                    status = 'COMPLETED'
                ORDER BY
                	end_time ASC;
                """

    conn = None
    try:

        conn = psycopg2.connect(**DB_KWARGS)  # Connect to DB
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)  # Get cursor
        cur.execute(command)  # Send the command

        # Returns just the top one. If there is no queued, this
        # value should be None.
        rows = cur.fetchall()

        cur.close()  # close communication with the PostgreSQL database server
        conn.commit()  # commit the changes

        return real_dicts_to_python_dicts(datetime_objs_to_strs(rows))

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
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)  # Get cursor
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


####### High level job control


def get_next_queued():
    """

    Get the next queued job from the DB, sorted by
    earliest submit_time. Returns the id.

    """

    queued_rows = get_all_queued()
    if len(queued_rows) > 0:
        return queued_rows[0]["id"]
    else:
        print("No queued jobs!")
        return None


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
            (datetime.datetime.now(), "QUEUED", project_name, git_url, git_user),
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
    ), "Status must be queued to start job, is currently: {}".format(job_row["status"])

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
    ), "Status must be running to end job, is currently: {}".format(job_row["status"])

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
