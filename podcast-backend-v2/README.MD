# Podcast Backend Prototype
The following repo will be used to prototype our new backend for our podcast app. See [`podcast-ios`](https://github.com/cuappdev/podcast-ios) for the client side code.

## Requirements

### Go
The app uses Go version 1.11. To install Go see [`Go Installation`](https://golang.org/doc/install)

#### Tooling
We use [`gometalinter`](https://github.com/alecthomas/gometalinter) for linting purposes and [`go mod`](https://github.com/golang/go/wiki/Modules) for vendoring.

### Docker
To run the app `Docker` and `Docker-Compose`  is required on your computer. See
[`Docker Installation`](https://docs.docker.com/install/) and
[`Docker Compose Installation`](https://docs.docker.com/compose/install/) for
installation steps.

## Running the app
To run the app you can run `make run`

## Testing
To test the app run `make test`

## Documentation
Documentation can be found by running `make docs` and then visiting
[`podcast-backend-v2 godocs`](http://localhost:6060/pkg/podcast-backend-proto/)
