FROM python:2.7
ADD service /service
ADD trainer /trainer
ADD start-server.sh /service/src
WORKDIR /service/
RUN pip install git+https://github.com/cuappdev/appdev.py.git --upgrade
RUN pip install -r requirements.txt
WORKDIR /service/src
