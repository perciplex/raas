FROM perciplex/raas-base:0.0.4

# Expose port for pyzmq
EXPOSE 5555
RUN git
# Get fresh clone of gym-raas
RUN git clone https://github.com/perciplex/gym-raas.git
RUN cd gym-raas && pip install -e . && cd  ..
# set hardware env variable
ENV RAASPI 1

# Set user and working directory
USER raas
WORKDIR /home/raas

# Clone repo to user_git_repo
ARG GIT_REPO_URL	
RUN git clone $GIT_REPO_URL user_git_repo	
CMD ["python3", "user_git_repo/run.py"]
