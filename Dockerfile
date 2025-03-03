
FROM continuumio/anaconda3:latest

RUN apt-get update && \
    apt-get clean;

RUN apt-get install git -y
RUN apt-get install gcc g++ -y

WORKDIR /home/transportal
ADD run.sh requirements.txt manage.py ./

RUN conda env create -c transportal-env python=3.6 -y
RUN echo "conda activate transportal-env" > ~/.bashrc
ENV PATH /opt/conda/envs/transportal-env/bin:$PATH
RUN pip install -r requirements.txt

ADD transportal transportal

RUN chmod +x run.sh
EXPOSE 8123

ENTRYPOINT "./run.sh"

