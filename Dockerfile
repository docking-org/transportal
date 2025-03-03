
FROM continuumio/anaconda3:latest

RUN apt-get update && \
    apt-get clean;

RUN apt-get install git -y
RUN apt-get install gcc g++ -y

WORKDIR /home/transportal
ADD run.sh environment.yml manage.py ./

RUN conda env create -f environment.yml 
RUN echo "conda activate transportal-env" > ~/.bashrc
ENV PATH /opt/conda/envs/transportal-env/bin:$PATH

ARG GIT_TOKEN=$GIT_TOKEN

ADD transportal transportal

RUN chmod +x run.sh
EXPOSE 8123

ENTRYPOINT "./run.sh"

