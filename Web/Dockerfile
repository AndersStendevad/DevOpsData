FROM python:3.8.5-slim-buster

COPY /itu_minitwit $HOME/itu_minitwit

WORKDIR $HOME/itu_minitwit

RUN export PYTHONPATH="${PYTHONPATH}:${HOME}/itu_minitwit"

RUN pip3 install -r requirements.txt


