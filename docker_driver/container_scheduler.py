import docker
import requests
import argparse
import time
from pathlib import Path

import re
import time

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

def write_led(msg):
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=4, block_orientation=90,rotate=2, blocks_arranged_in_reverse_order=True)
    show_message(device, msg, fill="white", font=proportional(LCD_FONT), scroll_delay=0.1)
    #device.contrast(intensity * 16)


def launch_docker(gitUrl="https://github.com/perciplex/raas-starter.git"):
    client = docker.from_env()

    dockerfile = str(Path(__file__).resolve().parent / "docker_images/final_image")
    docker_tag = "raas-dev-test:latest"

    write_led(gitUrl)

    print(dockerfile)
    print(docker_tag)
    print(gitUrl)

    # build the final image using the local raas-base, eventually need to pass in git url
    response = client.images.build(
        path=dockerfile, tag=docker_tag, buildargs={"GIT_REPO_URL": gitUrl}
    )

    # iniitializing docker container with dummy program. Is this how we should do it?
    container = client.containers.run(docker_tag, detach=True)

    try:
        output_data = container.get_archive("/usr/src/app/logs/")
    except Exception as e:
        print("Error {}".format(e))
        output_data = None

    print("StdOut: ", container)
    # print("Logs folder: ", output_data)
    # print("Docker Logs: ", container.logs())
    return str(container)

    """ok. When this program stops it kills the container.
    Ideally I'd like to create the ccontsiner and transfer
    files into it, then start it. But I can't figure out how?
    We could also build a custom dockerfile that is made from our base image.
    build and run that."""


parser = argparse.ArgumentParser(description="Parse incoming arguments.")
parser.add_argument(
    "-s", "--server", dest="server", default="http://raas.perciplex.com", help="Server IP address"
)

args = parser.parse_args()
server_ip = args.server

while True:
    try:
        response = requests.get(server_ip + "/job/pop")
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
        results = launch_docker(git_url)
        job_json["results"] = results
        requests.put(server_ip + "/job/%s/results" % job_id, json=job_json)
    else:
        # Wait and try again
        time.sleep(1)
