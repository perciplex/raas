FROM perciplex/raas-base:latest	

EXPOSE 8080

RUN adduser -D -u 1000 raas
USER raas

WORKDIR /home/raas

ARG GIT_REPO_URL	
RUN git clone $GIT_REPO_URL codeLocation	
CMD ["python", "codeLocation/run.py"]