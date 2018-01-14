# Local Environment Building/Testing
## 1. Have Docker running
```bash
> docker images
REPOSITORY           TAG                 IMAGE ID            CREATED              SIZE
```
## 2. Minikube Setup
```bash
> minikube start --insecure-registry=localhost:5000 --cpus 8 --disk-size 20g --memory 8000 --kubernetes-version v1.7.3
> minikube status
minikube: Running
cluster: Running
kubectl: Correctly Configured: pointing to minikube-vm at 192.168.99.100
```
You now have a single-noded Kubernetes cluster

## 3. Build Docker image and deploy to your Minikube environment
```bash
> minikube docker-env
export DOCKER_TLS_VERIFY="1"
export DOCKER_HOST="tcp://192.168.99.100:2376"
export DOCKER_CERT_PATH="/Users/<USER_NAME>/.minikube/certs"
export DOCKER_API_VERSION="1.23"
# Run this command to configure your shell:
# eval $(minikube docker-env)
> eval $(minikube docker-env)
> ls
Dockerfile README.md  service    trainer
> docker build -t podcast-ml-service:latest -f Dockerfile .
```
## 4. Deploying the service in Kubernetes
### 4a. Must put .env as a secret for the Pod
You need to execute:
```bash
> kubectl create secret generic podcast-secret --from-file=.env
```
to create the secret in the Kubernetes namespace so that all pods will have access
to the .env
### 4b. Ensure that redis service is up
This is done by going to the devops/redis/kubernetes and launching the helm chart.

### 4c. Deploy the service with a helm chart
This is done by running in the deployments:
```bash
> helm init
$HELM_HOME has been configured at /Users/<USERNAME>/.helm.

Tiller (the helm server side component) has been installed into your Kubernetes Cluster.
Happy Helming!
> ls
Dockerfile README.md  deployment service    trainer
> helm install --name podcast-ml deployment
NAME:   podcast-ml
LAST DEPLOYED: _____
NAMESPACE: default
STATUS: DEPLOYED

RESOURCES:
==> v1/Service
NAME     CLUSTER-IP  EXTERNAL-IP  PORT(S)         AGE
podcast  10.0.0.172  <pending>    5000:31720/TCP  0s

==> v1/ReplicationController
NAME     DESIRED  CURRENT  READY  AGE
podcast  1        1        0      0s
```

## 5. Service is now up and endpoints are able to be hit
# Production Environment Deployment
Identical to above but on GCE with multi-nodes. Instructions are the same.
