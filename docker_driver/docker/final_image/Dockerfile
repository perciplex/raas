FROM perciplex/raas-base:latest	

COPY . /app	

WORKDIR /app	

ARG GIT_REPO_URL	
RUN git clone $GIT_REPO_URL codeLocation	
CMD ["python", "codeLocation/app.py"]