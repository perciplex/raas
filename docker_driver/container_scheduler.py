import docker
import requests
import argparse
import time
from pathlib import Path
import json
import socket
import os
from led_driver import LedMessage
import upload_s3_utils

import reset_pendulum
from configparser import ConfigParser

config = ConfigParser()
config.read("/home/pi/config.ini")
FLASK_PASS = config.get("CREDS", "FLASK_PASS")


def launch_docker(git_url, job_id):
    client = docker.from_env()

    dockerfile = str(Path(__file__).resolve().parent / "docker_images/final_image")
    docker_tag = "raas-dev-test:latest"

    print(dockerfile)
    print(docker_tag)
    print(git_url)

    with open("/tmp/log.json", "w") as f:
        pass

    os.chmod("/tmp/log.json", 0o777)

    # build the final image using the local raas-base, eventually
    # need to pass in git url
    response = client.images.build(
        path=dockerfile,
        tag=docker_tag,
        buildargs={"GIT_REPO_URL": git_url},
        nocache=True,
    )

    # try to make the internal network which disables external
    # network traffic, fails gracefully
    try:
        client.networks.create(
            "docker_internal", driver="bridge", internal=True, check_duplicate=True,
        )
    except docker.errors.APIError:
        pass

    failed = False
    data = None

    try:
        stdout = client.containers.run(
            docker_tag,
            mounts=[
                {"Type": "bind", "Source": "/tmp/", "Target": "/tmp/", "RW": True,}
            ],
            network="docker_internal",
            # auto_remove=True,
            mem_limit="3g",
        )

    except docker.errors.ContainerError as e:
        print(dir(e.container))
        stdout = e.container.logs()
        failed = True
        print(stdout)
    except Exception as e:
        stdout = e
        failed = True
        print(stdout)

    try:
        with open("/tmp/log.json") as f:
            data = json.load(f)

        upload_s3_utils.upload_results("/tmp/log.json", "{}.json".format(job_id))

    except Exception as e:
        print(f"Error {e}")

    client.containers.prune()  # prune containers
    for image in filter(
        lambda image: not any(["perciplex/raas-base" in tag for tag in image.tags]),
        client.images.list(),
    ):  # clean images
        client.images.remove(image.id)

    return str(stdout), data, failed

    """ok. When this program stops it kills the container.
    Ideally I'd like to create the ccontsiner and transfer
    file into it, then start it. But I can't figure out how?
    We could also build a custom dockerfile that is made from our base image.
    build and run that."""


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

# clear LED screen
LedMessage(f"").stop()

while True:
    try:
        response = requests.get(
            server_ip + "/job/pop",
            params={"FLASK_PASS": FLASK_PASS, "hardware": socket.gethostname(),},
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
        print(job_json)
        job_id = job_json["id"]
        git_url = job_json["git_url"]
        user = job_json["git_user"]
        name = job_json["project_name"]

        led = LedMessage(f"{user}:{name}")
        led.start()

        stdout, data, failed = launch_docker(git_url, job_id)
        print("resetting")
        reset_pendulum.reset_pendulum()

        led.stop()

        # stdout, data = results.split("## STARTING DATA SECTION ##")
        # data = data.split("## ENDING DATA SECTION ##")[0]
        # print(data)
        # data = json.loads(data)

        job_json["stdout"] = stdout
        job_json["data"] = data  # data
        job_json["failed"] = failed
        requests.put(
            server_ip + "/job/%s/results" % job_id,
            params={"FLASK_PASS": FLASK_PASS},
            json=job_json,
        )
    else:
        # Wait and try again
        time.sleep(1)
