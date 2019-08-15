import docker
import tarfile
client = docker.from_env()

#logs = client.containers.run("raas", "python test_script.py")
#print(logs) #logs is standard out



container = client.containers.run("raas",detach=True)
print("loading file")

# make a tar file
# https://stackoverflow.com/questions/46390309/how-to-copy-a-file-from-host-to-container-using-docker-py-docker-sdk
# tar -cvf test_script.tar test_script2.py 
data = open("test_script.tar", 'rb').read()
container.put_archive("/usr/src/app", data)
print("executing script")
exit_code, output = container.exec_run("python test_script2.py")
print(output)
input()
exit_code, output = container.exec_run("ls")
print(output)
#container.exec_run("python test_script2.py") 

#data = container.get_archive("/usr/src/app/logs/")

#  container.exec_run("echo hello")
#
print(output)
#input()
print(container.logs())
