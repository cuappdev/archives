FROM node:6

RUN mkdir /usr/src/app
RUN git clone https://github.com/cuappdev/tcat.js.git /usr/src/app

WORKDIR /usr/src/app
RUN git checkout austin/routingOptimizations
RUN npm install

RUN mkdir tcat-ny-us
WORKDIR /usr/src/app/tcat-ny-us
RUN wget https://s3.amazonaws.com/tcat-gtfs/tcat-ny-us.zip
RUN apt-get update
RUN apt-get install unzip
RUN unzip tcat-ny-us.zip

WORKDIR /usr/src/app
RUN ./node_modules/webpack/bin/webpack.js -p

EXPOSE 3000
CMD npm run serve

