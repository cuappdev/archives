FROM openjdk:8

RUN mkdir /usr/src/app
RUN git clone https://github.com/cuappdev/tcat-map.git /usr/src/app

WORKDIR /usr/src/app

RUN apt-get update

RUN apt-get -y install maven wget


RUN git clone https://github.com/graphhopper/graphhopper.git /ghopper-walking


WORKDIR /usr/src/app/ghopper-walking/graphhopper
RUN ./graphhopper.sh buildweb

WORKDIR /usr/src/app

EXPOSE 8987

CMD java -Xmx1g -Xms1g -jar ghopper-walking/graphhopper/web/target/graphhopper-web-*-with-dep.jar datareader.file=osrm/map.osm jetty.port=8987 jetty.resourcebase=./graphhopper/web/src/main/webapp graph.flag_encoders=foot prepare.ch.weightings=no graph.location=ghopper-walking/graph-cache

