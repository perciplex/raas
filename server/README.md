swagger: '2.0'
info:
  description: |
    Rass API
  version: 1.0.0
  title: RaaS

paths:
  /job:
    get:
      tags:
      - external
      summary: Get a list of active jobs
      responses:
        200:
          description: Successful operation
          schema:
            type: array
            items:
              $ref: '#/definitions/Job'
    post:
      tags:
      - external
      summary: Add a job to the queue
      parameters:
      - in: body
        name: job
        required: true
        schema:
          $ref: '#/definitions/Results'
      responses:
        200:
          description: Successful operation
        400:
          description: Invalid git repo supplied
  /job/pop:
    get:
      tags:
      - internal
      summary: Get a job to do
      responses:
        200:
          description: Successful operation
          schema:
            $ref: '#/definitions/Job'
        204:
          description: No jobs available
  /job/{jobId}/start:
    put:
      tags:
      - internal
      summary: Update a job status
      parameters:
      - name: jobId
        in: path
        description: ID of job to update
        required: true
        type: string
      responses:
        200:
          description: Successful operation
        404:
          description: Job not found
  /job/{jobId}/results:
    put:
      tags:
      - internal
      summary: Update a job results
      parameters:
      - name: jobId
        in: path
        description: ID of job to update
        required: true
        type: string
      - name: results
        in: body
        description: New results
        required: true
        schema:
          $ref: '#/definitions/Results'
      responses:
        200:
          description: Successful operation
        404:
          description: Job not found
    get:
      tags:
      - external
      summary: Get job results
      parameters:
      - name: jobId
        in: path
        description: ID of job to update
        required: true
        type: string
      responses:
        200:
          description: Successful operation
          schema:
            $ref: '#/definitions/Results'

definitions:
  Job:
    type: object
    properties:
      id:
        type: integer
        description: automatically assigned job id
      gitUrl:
        type: string
        description: url for a public git repo containing the job files
      status:
        type: string
        description: job status
        enum:
        - queued
        - running
        - complete
        default: queued
  Results:
    type: object
    properties:
      results:
        type: string
      
# Added by API Auto Mocking Plugin
host: virtserver.swaggerhub.com
basePath: /ishmandoo/RaaS/1.0.0
schemes:
 - https
