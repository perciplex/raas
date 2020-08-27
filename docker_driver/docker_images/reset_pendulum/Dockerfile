FROM perciplex/raas-base:0.0.4

# Expose port for pyzmq
#EXPOSE 5555

# Get fresh clone of gym-raas
RUN git clone https://github.com/perciplex/gym-raas.git && cd gym-raas && pip3 install -e . && cd  ..

# set hardware env variable
ENV RAASPI 1

# Set user and working directory
USER raas


WORKDIR /home/raas

ADD reset_pendulum.py reset_pendulum.py
# Run reset pendulum.py
CMD ["python3", "reset_pendulum.py"]
