FROM openjdk:8

RUN mkdir /usr/src/app
RUN git clone https://github.com/cuappdev/tcat.js.git /usr/src/app

WORKDIR /usr/src/app
RUN git checkout austin/realtime
RUN apt-get update

RUN apt-get -y install maven wget
RUN sh scripts/setup.sh

WORKDIR /usr/src/app/graphhopper
RUN ./graphhopper.sh buildweb

WORKDIR /usr/src/app
RUN cp tcat-ny-us/tcat-ny-us.zip .

EXPOSE 8988

CMD java -Xmx1g -Xms1g -jar graphhopper/web/target/graphhopper-web-*-with-dep.jar datareader.file=osrm/map.osm gtfs.file=tcat-ny-us.zip jetty.port=8988 jetty.resourcebase=./graphhopper/web/src/main/webapp graph.flag_encoders=pt prepare.ch.weightings=no graph.location=./graph-cache
