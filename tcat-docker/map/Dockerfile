FROM openjdk:8

RUN mkdir /usr/src/app
RUN git clone https://github.com/cuappdev/tcat.js.git /usr/src/app

WORKDIR /usr/src/app
RUN git checkout austin/realtime
RUN apt-get update

RUN apt-get -y install maven wget
RUN sh scripts/setup.sh

WORKDIR /usr/src/app
RUN cp tcat-ny-us/tcat-ny-us.zip .

WORKDIR /usr/src/app/map-matching

EXPOSE 8989

CMD ./map-matching.sh action=start-server
