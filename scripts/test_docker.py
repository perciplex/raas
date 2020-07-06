import json
import os
from pathlib import Path

import docker


def launch_docker(gitUrl="https://github.com/perciplex/raas-starter.git"):
    client = docker.from_env()

    dockerfile = str(Path(__file__).resolve().parent / "docker_images/final_image")
    docker_tag = "raas-dev-test:latest"

    print(dockerfile)
    print(docker_tag)
    print(gitUrl)

    with open("/tmp/log.json", "w") as f:
        pass

    os.chmod("/tmp/log.json", 0o777)

    # build the final image using the local raas-base, eventually need to pass in git url
    response = client.images.build(
        path=dockerfile,
        tag=docker_tag,
        buildargs={"GIT_REPO_URL": gitUrl},
        nocache=True,
    )

    # try to make the internal network which disables external network traffic, fails gracefully
    try:
        client.networks.create(
            "docker_internal", driver="bridge", internal=True, check_duplicate=True
        )
    except docker.errors.APIError:
        pass

    failed = False
    data = None

    try:
        stdout = client.containers.run(
            docker_tag,
            mounts=[{"Type": "bind", "Source": "/tmp/", "Target": "/tmp/", "RW": True}],
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

    except Exception as e:
        print(f"Error {e}")

    return str(stdout), data, failed

    """ok. When this program stops it kills the container.
    Ideally I'd like to create the ccontsiner and transfer
    file into it, then start it. But I can't figure out how?
    We could also build a custom dockerfile that is made from our base image.
    build and run that."""


res = launch_docker("https://github.com/perciplex/raas-starter.git")
print(res)
