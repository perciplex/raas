#!/usr/bin/python

import psycopg2

"""

This is a script for quickly destroying and recreating the jobs table.
It has to drop both the statuses type and the table. This makes it easy to
just "start over" the table if we want to change columns or something.


"""

DB_KWARGS = {
    "database": "postgres",
    "user": "perciplex",
    "password": "TVaH5aKw3iEAenP",
    "host": "raas-jobs.c0cgyyikkgwi.us-east-2.rds.amazonaws.com",
    "port": "5432",
}


def recreate_table():

    commands = (
        """
        DROP TABLE IF EXISTS jobs;
        """,
        """
        DROP TYPE IF EXISTS statuses;
        """,
        """
        CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
        """,
        """
        CREATE TYPE statuses AS ENUM ('queued', 'running', 'completed', 'failed');
        """,
        """
        CREATE TABLE jobs (

            id uuid PRIMARY KEY DEFAULT uuid_generate_v4 (),
            submit_time TIMESTAMPTZ NOT NULL,
            start_time TIMESTAMPTZ,
            end_time TIMESTAMPTZ,
            status statuses,
            project_name TEXT NOT NULL,
            git_url TEXT NOT NULL,
            git_user TEXT NOT NULL,
            hardware_name TEXT
        )
        """,
    )
    #             id SERIAL PRIMARY KEY,
    conn = None
    try:
        print("trying to connect...")
        conn = psycopg2.connect(**DB_KWARGS)
        print("Connected!")
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            print("Executing:")
            print(command)
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    recreate_table()
