import docker
import requests
import argparse
import time
def launch_docker(gitUrl="https://github.com/perciplex/raas-starter.git"):
    client = docker.from_env()
    dockerfile = "docker/."
    docker_tag = "raas-dev-test:latest"

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
    print("Logs folder: ", output_data)
    print("Docker Logs: ", container.logs())
    return str(container.logs())

    """ok. When this program stops it kills the container.
    Ideally I'd like to create the ccontsiner and transfer
    files into it, then start it. But I can't figure out how?
    We could also build a custom dockerfile that is made from our base image.
    build and run that."""


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument(
        "-s", "--server", dest="server", default="localhost", help="Server IP address"
    )

args = parser.parse_args()
server_ip = args.server

while True:

    response = requests.get(server_ip + "/job/pop")
    if response.status_code == 204:
        time.sleep(1)
    else:
        job_json = response.json()
        id = job_json["id"]
        gitUrl = job_json["gitUrl"]
        #{"id": self.id, "gitUrl":self.git, "results":self.results, "status":self.status}
        results = launch_docker(gitUrl)
        job_json["results"] = results
        requests.put('/job/%d/results' % id, json=job_json) #json or data?

