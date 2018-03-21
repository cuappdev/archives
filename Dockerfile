FROM python:2.7

RUN mkdir /usr/src/app
RUN git clone https://github.com/cuappdev/register.git /usr/src/app

WORKDIR /usr/src/app

RUN pip install -r requirements.txt
RUN pip install git+https://github.com/cuappdev/appdev.py.git --upgrade

WORKDIR src/client
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -
RUN apt-get install -y nodejs
RUN npm install
WORKDIR ../../

EXPOSE 5000
CMD sh src/scripts/start_server.sh
