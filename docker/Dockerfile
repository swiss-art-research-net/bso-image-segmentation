FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install -y curl \
    git \
    python3.6 \
    python3-distutils \
    python3-apt \
    libgl1-mesa-glx \
    libglib2.0-0


RUN echo "alias python=python3.6" >> ~/.bashrc
RUN curl https://bootstrap.pypa.io/get-pip.py | python3.6

RUN pip3 install notebook opencv-python
RUN pip3 install git+https://github.com/dhlab-epfl/dhSegment
RUN pip3 install tensorflow==1.13.1
RUN pip3 install PYyaml SPARQLWrapper tqdm

RUN mkdir workdir
VOLUME /workdir
WORKDIR /workdir

CMD ["bash", "-c", "source /etc/bash.bashrc && jupyter notebook --notebook-dir=/workdir --ip 0.0.0.0 --no-browser --allow-root  --NotebookApp.token='' --NotebookApp.password=''"]