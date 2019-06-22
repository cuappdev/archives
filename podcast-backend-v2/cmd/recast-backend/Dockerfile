FROM golang:1.11

ADD . /usr/local/go/podcast-backend-v2
WORKDIR /usr/local/go/podcast-backend-v2/cmd/recast-backend
RUN go build
CMD /usr/local/go/podcast-backend-v2/cmd/recast-backend/recast-backend
