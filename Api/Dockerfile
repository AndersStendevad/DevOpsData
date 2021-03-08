FROM python:3.8.5-slim-buster

COPY /minitwitAPI $HOME/minitwitAPI

WORKDIR $HOME/minitwitAPI

RUN pip3 install -r requirements.txt

RUN export PYTHONPATH="${PYTHONPATH}:${HOME}/minitwitAPI"

COPY start.sh $HOME/minitwitAPI
RUN chmod +x start.sh
