FROM python:3.8.5-slim-buster

# copy all the files from here into image /src/
COPY /itu-minitwit $HOME/itu-minitwit

ADD minitwit.db $HOME/

RUN pip3 install -r /itu-minitwit/requirements.txt

EXPOSE 5000
WORKDIR $HOME/src/
CMD ["python3", "/itu-minitwit/minitwit.py"]