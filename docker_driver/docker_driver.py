import docker

client = docker.from_env()

# dockerfile path and tags
dockerfile = "docker/."
docker_tag = "raas-dev-test:latest"
git_url = "https://github.com/perciplex/raas-starter.git"

# build the final image using the local raas-base, eventually need to pass in git url
response = client.images.build(
    path=dockerfile, tag=docker_tag, buildargs={"GIT_REPO_URL": git_url}
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

"""ok. When this program stops it kills the container.
Ideally I'd like to create the ccontsiner and transfer
files into it, then start it. But I can't figure out how?
We could also build a custom dockerfile that is made from our base image.
build and run that.

"""
