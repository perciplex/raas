FROM ubuntu:18.04
RUN apt-get update
RUN apt-get install -y libhdf5-dev libc-ares-dev libeigen3-dev \
                           gcc gfortran python-dev libgfortran5 \
                          libatlas3-base libatlas-base-dev libopenblas-dev \
                           libopenblas-base libblas-dev \
                          liblapack-dev cython libatlas-base-dev openmpi-bin \
                          libopenmpi-dev python3.7-dev python3.7 python3.7-distutils \
                          wget curl libzmq3-dev git
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 2
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3.7 get-pip.py
RUN rm get-pip.py
RUN pip3 install keras_applications==1.0.8 --no-deps
RUN pip3 install keras_preprocessing==1.1.0 --no-deps
RUN pip3 install h5py==2.9.0
RUN pip3 install pybind11
RUN pip3 install -U --user six wheel mock
# https://github.com/PINTO0309/Tensorflow-bin/#usage
RUN wget "https://raw.githubusercontent.com/PINTO0309/Tensorflow-bin/master/tensorflow-2.3.1-cp37-none-linux_armv7l_download.sh"
RUN chmod +x ./tensorflow-2.3.1-cp37-none-linux_armv7l_download.sh
RUN ./tensorflow-2.3.1-cp37-none-linux_armv7l_download.sh
RUN rm ./tensorflow-2.3.1-cp37-none-linux_armv7l_download.sh
RUN pip3 uninstall tensorflow
RUN pip3 install https://www.piwheels.org/simple/grpcio/grpcio-1.32.0-cp37-cp37m-linux_armv7l.whl#sha256=30c04a03494beb37ded4238602d92372718f19538a7cb804b32847da3d26f17d
RUN pip3 install tensorflow-2.3.1-cp37-none-linux_armv7l.whl



RUN wget "https://github.com/radimspetlik/pytorch_rpi_builds/raw/master/torch/torch-1.5.0a0%2B4ff3872-cp37-cp37m-linux_armv7l.whl"
RUN pip install torch-1.5.0a0+4ff3872-cp37-cp37m-linux_armv7l.whl

# Binary install pyzmq
RUN pip3 install --no-binary :all: pyzmq==18.1.0
# Copy and install requirements.txt
COPY requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt
# Create raas user and provide codeLocation directory
RUN groupadd -r raas && useradd -r -g raas raas && mkdir -p /home/raas/user_git_repo && chown raas /home/raas/user_git_repo
