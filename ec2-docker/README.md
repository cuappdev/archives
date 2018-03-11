# EC2 Docker - Deployment Tool

This is a tool for testing and deploying our backends to production environments. This is a Vagrant machine that installs Ansible and uses it to deploy a Docker Compose onto an EC2 Instance.

## Credits

We use the following Ansible roles from fellow open source developers.
* [angstwad/docker.ubuntu](https://github.com/angstwad/docker.ubuntu) - renamed to "docker" in our roles directory

## Install

To install on Linux
```
sudo apt-get install software-properties-common
sudo apt-add-repository ppa:ansible/ansible
sudo apt-get update
sudo apt-get install ansible
```

To install on macOS (_supposedly_)
```
sudo pip install ansible
```