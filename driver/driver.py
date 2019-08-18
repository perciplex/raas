import docker
import tarfile
import time
import git
import os
import shutil

client = docker.from_env()

# clone the repo into
repo_dir = "./temp/git"
tar_name = "./temp/package.tar"


#cleanup temp folder
#shutil.rmtree("./temp")

repo = git.Repo.clone_from("https://gist.github.com/a7ae5925ac4ace2292fa6fe192a56723.git",repo_dir)

# make tar of git. Is this ridiculous?
with tarfile.open(tar_name, "w:gz") as tar_handle:
    tar_handle.add(repo_dir,arcname="")


# iniitializing docker container with dummy program. Is this how we should do it?
container = client.containers.run("raas" , 'sleep 5s', detach=True)

print("putting tar into docker")
data = open(tar_name, 'rb').read()
container.put_archive("/usr/src/app", data)

print("executing script")
exit_code, output = container.exec_run("python app.py")

try:
    output_data = container.get_archive("/usr/src/app/logs/")
except:
    output_data = None

print("StdOut: ", output)
print("Logs folder: ", output_data)
print("Docker Logs: ", container.logs())

#cleanup temp folder
shutil.rmtree("./temp")







## TRRRRRRRAAAAAASSSSSHHHH

'''
while container.status != 'running':
    print(container.status)
    #container.start()
    time.sleep(0.1)
'''

'''
for root, dirs, files in os.walk(repo_dir):
    for file in files:
        tar_handle.add(os.path.join(root, file))
'''

#logs = client.containers.run("raas", "python test_script.py")
#print(logs) #logs is standard out

# or should we build a new dockerfile?
# based in raas
#with a run statement
dockerfile = '''
FROM raas
RUN git pull {repo}
CMD python3 app.py
'''
# import io
# io.StringIO(dockerfile.format(repo=repo))
# HOOOOO BOY THAT"S BAD TO DO IT THAT WAY. unsanitized running of user strings?! yeesh
# docker.image.build


'''ok. When this program stops it kills the container.
Ideally I'd like to create the ccontsiner and transfer 
files into it, then start it. But I can't figure out how?
We could also build a custom dockerfile that is made from our base image.
build and run that.

'''


