import argparse
import json
import os
import socket
import time
from configparser import ConfigParser
from pathlib import Path

import requests
import reset_pendulum
import upload_s3_utils
from docker import DockerClient
from docker.errors import APIError, BuildError, ContainerError
from led_driver import LedMessage

config = ConfigParser()
config.read("/home/pi/config.ini")
FLASK_PASS = config.get("CREDS", "FLASK_PASS")


def launch_docker(client, git_url, job_id):

    dockerfile = str(Path(__file__).resolve().parent / "docker_images/final_image")
    docker_tag = "raas-dev-test:latest"

    print(dockerfile)
    print(docker_tag)
    print(git_url)

    failed = False
    data = None

    with open("/tmp/log.json", "w") as f:
        pass

    os.chmod("/tmp/log.json", 0o777)

    # build the final image using the local raas-base
    try:
        client.images.build(
            path=dockerfile,
            tag=docker_tag,
            buildargs={"GIT_REPO_URL": git_url},
            nocache=True,
        )
    except BuildError as e:
        stdout = e
        failed = True
        print("Error building image! Aborting.\n{}".format(e))
        return str(stdout), data, failed

    # try to make the internal network which disables external
    # network traffic, fails gracefully
    try:
        client.networks.create(
            "docker_internal",
            driver="bridge",
            internal=True,
            check_duplicate=True,
            scope="local",
        )
    except APIError as e:
        stdout = e
        failed = True
        print("Error creating network! Aborting.\n{}".format(e))
        return str(stdout), data, failed

    try:
        stdout = client.containers.run(
            docker_tag,
            mounts=[{"Type": "bind", "Source": "/tmp/", "Target": "/tmp/", "RW": True}],
            network="docker_internal",
            mem_limit="3g",
        )
    except ContainerError as e:
        print(dir(e.container))
        stdout = e.container.logs()
        failed = True
        print("Error running container! Aborting.\n{}".format(e))
        return str(stdout), data, failed
    except Exception as e:
        stdout = e
        failed = True
        print(stdout)
        return str(stdout), data, failed

    try:
        with open("/tmp/log.json", "r") as f:
            data = json.load(f)
            data["stdout"] = str(stdout)

    except Exception as e:
        print(f"Error {e}")

    return str(stdout), data, failed


def cleanup_images(client):
    """
    Stops all containers, prunes, and cleans up images except raas-base

    Args:
    client (DockerClient): Docker client object for env
    """
    # Stop all containers.
    for container in client.containers.list():
        container.stop()

    # Prune containers
    client.containers.prune()

    # Remove all images except `raas-base`
    for image in filter(
        lambda image: not any(["perciplex/raas-base" in tag for tag in image.tags]),
        client.images.list(),
    ):
        client.images.remove(image.id)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse incoming arguments.")
    parser.add_argument(
        "-s",
        "--server",
        dest="server",
        default="http://raas.perciplex.com",
        help="Server IP address",
    )

    args = parser.parse_args()
    server_ip = args.server

    # Instantiate docker client
    docker_client = DockerClient.from_env()

    # clear LED screen
    LedMessage(f"").stop()

    while True:
        try:
            response = requests.get(
                server_ip + "/job/pop",
                params={"FLASK_PASS": FLASK_PASS, "hardware": socket.gethostname()},
            )
            response_status = response.status_code
            print(response)
        except requests.exceptions.ConnectionError as e:
            response_status = None
            print("Server not reached {}".format(e))

        # If work is found, launch the work
        if response_status == 200:
            # Get response json
            job_json = response.json()
            job_id = job_json["id"]
            git_url = job_json["git_url"]
            user = job_json["git_user"]
            name = job_json["project_name"]

            led = LedMessage(f"{user}:{name}")
            led.start()

            print("Launching docker image")
            stdout, data, failed = launch_docker(docker_client, git_url, job_id)
            led.stop()

            print("Uploading results to S3")
            upload_s3_utils.upload_string(job_id, json.dumps(data))

            print("Resetting pendulum")
            reset_pendulum.reset_pendulum()

            print("Cleaning images")
            cleanup_images(docker_client)

            job_json["stdout"] = stdout
            job_json["data"] = data
            job_json["failed"] = failed

            print("Returning status to webserver")
            requests.put(
                server_ip + "/job/%s/results" % job_id,
                params={"FLASK_PASS": FLASK_PASS},
                json=job_json,
            )
            print("Job done.")
        else:
            # Wait and try again
            time.sleep(2)
