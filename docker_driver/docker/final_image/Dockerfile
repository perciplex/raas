FROM perciplex/raas-base:0.0.4	

EXPOSE 8080

RUN groupadd -r raas && useradd -r -g raas raas

WORKDIR /home/raas

RUN mkdir -p codeLocation && chown raas codeLocation

USER raas

ARG GIT_REPO_URL	
RUN git clone $GIT_REPO_URL codeLocation	
CMD ["python3", "codeLocation/run.py"]
