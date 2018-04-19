# EC2 Docker - Deployment Tool

This is a tool for testing and deploying our backends to production environments. Thi uses *Ansible* deploy a *Docker Compose* onto an *Ubuntu 16.04 EC2 instance*. For simple single node deployments, use this tool to deploy a backend.

We use Ubuntu 16.04 for its ubiquity and widespread community support. We use Ansible to install Docker and the tools necessary to use Docker Compose, and also autoclean previous deployments, and automatically boot up the latest revision of a backend. 

## Requirements

The tool requires 3 pieces of information supplied by the developer to operate
* A `docker-compose.yml` and the associated `Dockerfile`s at the directory `./docker-compose/`
    * One of the containers should be mapped to the machine's port 80 to accept HTTP requests
* A `hosts` file containing the IP address of the EC2 instance placed in this directory
* A `server.pem` file containing the EC2's instances private key in the current directory

Ansible uses the `hosts` file to determine which machines to provision based on their IP address. It will automatically install Docker and Docker Compose if it isn't there and proceed to clean up any previous deployments (by killing and removing all containers and images). It will then use `docker-compose.yml` to boot up all the containers required to run the backend.

## Instructions

After installing Ansible (see below), you simply need to run the following command in the current directory.
```
ansible-playbook site.yml
```

## Install Ansible on Linux and macOS

To install Ansible on Linux
```
sudo apt-get install software-properties-common
sudo apt-add-repository ppa:ansible/ansible
sudo apt-get update
sudo apt-get install ansible
```

To install Ansible on macOS (_supposedly_)
```
sudo pip install ansible
```

## Install Ansible on Windows

To use Ansible on Windows, we use Vagrant to set up a Linux box that has Ansible installed. First, install Vagrant and Virtualbox. Then, install a series of plugins that make your life easier.
```
vagrant plugin install vagrant-vbguest
```

Then, in this directory:
```
vagrant up
vagrant ssh
```

You'll have access to a machine that can deploy to the EC2 Instance.
