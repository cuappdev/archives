# Ansible + Docker - Deployment Tool

This is a tool for deploying our backends to production environments. It uses *Ansible* deploy a *Docker Compose* onto an *Ubuntu 16.04 machine*. The goal is to minimize the developer's job to perfecting a Docker Compose and the associated Dockerfiles, so that these tools can deploy those microservices quickly and easily.

We use Ubuntu 16.04 for its ubiquity and widespread community support. We use Docker to create sandboxed containers for our backends/microservices, and Docker Compose to orchestrate multiple Docker containers. We use Ansible to install Docker and Docker Compose, autoclean previous deployments, and automatically boot up the latest revision of a backend. 

## Requirements

The tool requires 3 pieces of information supplied by the developer to operate
* A `docker-compose.yml` and the associated `Dockerfile`s at the directory `./docker-compose/`
    * One of the containers *must* be mapped to the machine's port 80 to accept HTTP requests
* A `hosts` file containing the IP address of the machine placed in this directory
* A `server.pem` file containing the machine's private key in the current directory

Ansible uses the `hosts` file to determine which machines to provision based on their IP address. It will automatically install Docker and Docker Compose if it isn't there and proceed to clean up any previous deployments (by killing and removing all containers and images). It will then use `docker-compose.yml` to boot up all the containers required to run the backend. The `server.pem` is necessary to SSH into the machine.

## Instructions

### Setting up the machine

After installing Ansible (see below), you need to set the correct permissions for the `server.pem` file, and set up the machine for rapid deployment.
```
chmod 0400 server.pem
ansible-playbook setup.yml
```

### Deploying

Once the machine has been set up as above, you can deploy using Ansible:
```
ansible-playbook deploy.yml
```

### Windows 10 caveats

If you are deploying from Windows 10 using a Vagrant box (see below), *before* any operations you *must* copy the tool's files into the Vagrant box's file system. By default, the contents of this directory is shared with the Vagrant box at `/deploy`. We cannot modify the `server.pem`'s permissions correctly on the shared filesystem. As such, before doing any of the above instructions, make sure to get the most recent configuration of the tool into the Vagrant box's filesystem at `~/deploy`.
```
rm -rf ~/deploy # If it already exists
cp -r /deploy ~
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

To use Ansible on Windows, we use Vagrant to set up a Linux box that has Ansible installed. First, install Vagrant and Virtualbox. Then, install the Virtualbox file sharing plugin:
```
vagrant plugin install vagrant-vbguest
```

After that initial setup, in this directory:
```
vagrant up
vagrant ssh
```

You'll have access to a machine that can deploy to a machine.