# DevOps

This repository includes all developer operations for `AppDev` projects.

## Ansible + Docker

We are moving towards deploying our backends using Docker containers. As such, we must ready our machines for use with Docker and Docker Compose, so we can easily deploy single node, multi-container backends. Take a look at the `ansible-docker` folder for the tool we use to deploy our backends.

## Environment Variables

If your project involves sensitive information, keep that information as environment variables. We intentionally do not push environment variables to our public repositories, and instead aim to supply them to our deployments via Docker Compose. For local development, we recommend you find a way to load the environment variables automatically after booting up the backend.
