## driver

We need a driver program that will 

1. poll the server for new gists
2. run a docker container
3. return the standard out or pickle (less than 1mb?)

run `python3 driver.py` to pull a test repo and run it in a docker container.
WARNING: WILL DESTROY ./TEMP FOLDER