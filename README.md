# RaaS

<img src="server/static/logo.png" alt="Your image title" width="200"/><img src="server/static/pplex_logo_wordmark.png" alt="Your image title" width="150"/>

![pendulum swing up](swingup.gif)

Reality as a Service (RaaS) is an open source platform for hosting physical OpenAI Gym environments. This lowers the barrier to transitioning to real robots in both effort and cost, allows the outsourcing of mantainance of robots to specialists, amoritiized cost of robots over more researchers and RL practitioners, and less useless down-time for expensive robots.

The user submits a git repo to a web based frontend. The queue is queried by robot instances, which then gives the user an allotted amount of time. The results of this run are then returned to the user.

The robot is controlled via a gym enviroment top be found [here](https://github.com/perciplex/raas-envs).

The system is not currently operational, but you can find the site at [raas.perciplex.com](http://raas.perciplex.com).

### Folder Summary

- `raas_gym` - Library that replicates opanai gym interface for both simulation testing and for running on physical hardware. This is the client facing code to be imported in python
- `server/` - Server aide application for accepting new jobs, amaintaining job queue, and returning data to web frontend.
- `hardware/` - contains bill of materials and instructions for constructing pendulum. Also contains python motor driver code.
- `docker_driver/` - Responsible for polling server, getting repo, cloning into docker image and running.

### Architecture Diagram

![](block_diagram.png)
