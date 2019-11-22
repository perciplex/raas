#FROM multiarch/qemu-user-static:x86_64-arm as qemu
#FROM arm32v7/ubuntu
FROM ubuntu
#COPY --from=qemu /usr/bin/qemu-arm-static /usr/bin

# Apt update and install dependencies
RUN apt-get update -y
RUN apt-get install -y \
    python3-pip \
    python3-numpy \
    python3-scipy \
    libzmq3-dev \
    git

# Binary install pyzmq
RUN pip3 install --no-binary :all: pyzmq==18.1.0

# Copy and install requirements.txt
COPY requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt

# Create raas user and provide codeLocation directory
RUN groupadd -r raas && useradd -r -g raas raas && mkdir -p /home/raas/user_git_repo && chown raas /home/raas/user_git_repo
