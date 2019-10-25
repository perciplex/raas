FROM python:3.7

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

ARG GIT_REPO_URL
RUN git clone $GIT_REPO_URL codeLocation
CMD ["python", "codeLocation/app.py"]