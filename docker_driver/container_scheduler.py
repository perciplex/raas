import docker
import requests
import argparse
import time
from pathlib import Path


def launch_docker(gitUrl="https://github.com/perciplex/raas-starter.git"):
    client = docker.from_env()

    dockerfile = str(Path.cwd() / 'docker_images/final_image')
    docker_tag = "raas-dev-test:latest"

    print(dockerfile)
    print(docker_tag)
    print(gitUrl)

    # build the final image using the local raas-base, eventually need to pass in git url
    response = client.images.build(
        path=dockerfile, tag=docker_tag, buildargs={"GIT_REPO_URL": gitUrl}
    )

    # iniitializing docker container with dummy program. Is this how we should do it?
    container = client.containers.run(docker_tag, detach=False)

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
    "-s", "--server", dest="server", default="localhost", help="Server IP address"
)

args = parser.parse_args()
server_ip = args.server

while True:
    server_ip = "http://raas.perciplex.com"
    response = requests.get(server_ip + "/job/pop")
    print(response)

    # If work is found, launch the work
    if response.status_code == 200:
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
