FROM perciplex/raas-base:latest	

COPY . /app	

WORKDIR /app	

RUN useradd -ms /bin/bash raas
USER raas

ARG GIT_REPO_URL	
RUN git clone $GIT_REPO_URL codeLocation	
CMD ["python", "codeLocation/run.py"]