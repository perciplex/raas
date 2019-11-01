FROM arm32v7/ubuntu

RUN apt-get update -y
RUN apt-get install python3-pip -y
RUN apt-get install python3-numpy -y
RUN apt-get install python3-scipy -y
RUN apt-get install git -y

COPY . /app
WORKDIR /app

RUN pip3 install -r requirements.txt

RUN git clone https://github.com/perciplex/gym-raas.git && cd gym_raas && pip install -e . && cd ..