## driver


We need a driver program that will 

1. poll the server for new git repos
2. run a docker container
3. return the standard out or pickle (less than 1mb?)

run `python3 driver.py` to pull a test repo and run it in a docker container.

Security Issues:
https://docs.docker.com/engine/security/security/
We need to try and restrict all privileges
Scrub any use input and be careful how it is used
Restrict the network connections of the pi
Change the pi root 
Run the program inside docker itself as an unprivileged user

https://github.com/remoteinterview/compilebox
https://github.com/christophetd/docker-python-sandbox

We need to wire in resource limits, just so no one does something funky
