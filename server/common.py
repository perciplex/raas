#!/usr/bin/python

class JobStatus:
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


JOB_STATUS_LIST = [
    JobStatus.QUEUED,
    JobStatus.RUNNING,
    JobStatus.COMPLETED,
    JobStatus.FAILED,
]
