#FROM multiarch/qemu-user-static:x86_64-arm as qemu
FROM arm32v7/ubuntu
#COPY --from=qemu /usr/bin/qemu-arm-static /usr/bin

RUN apt-get update -y

RUN apt-get install -y \
    python3-pip \
    python3-numpy \
    python3-scipy \
    libzmq3-dev \
    git 

RUN pip3 install --no-binary :all: pyzmq==18.1.0

COPY requirements.txt /app/requirements.txt
WORKDIR /app

RUN pip3 install -r requirements.txt

RUN git clone https://github.com/perciplex/gym-raas.git && cd gym-raas && pip3 install -e . && cd ..
