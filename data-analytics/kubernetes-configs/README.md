# Deploying Couchbase with Kubernetes on AWS

Most of what is documented in this page can also be found [here](http://blog.kubernetes.io/2016/08/create-couchbase-cluster-using-kubernetes.html).

To get started, you should install Kubernetes. You can download a pre-built binary [here](https://kubernetes.io/docs/getting-started-guides/binary_release/). I would not recommend using the brew tool since it does not come with tools for creating a cluster. Next, use `cd` to navigate into the `kubernetes` directory you just downloaded.

## Starting a Kubernetes cluster
This step creates kubernetes server nodes on AWS. If you already have a kubernetes cluster running on AWS, you don't need to create a new cluster. Refer to [Autoscaling a Kubernetes Cluster](#autoscaling-a-kubernetes-cluster) if you need to increase the number of nodes in the cluster.

Make sure kubernetes knows what your desired cloud provider is by running: `export KUBERNETES_PROVIDER=aws`. You can also save that line to your `~/.bash_profile` to maintain the environment variable across terminal sessions. Additionally, create/download an AWS credentials file from AppDev's AWS account and save it as `~/.aws/credentials`.

Now, we are ready to deploy a cluster. For this example, we will be deploying a cluster with 1 master and 2 minions. From within the `kubernetes` directory, we'll run

```
KUBE_AWS_ZONE=us-west-2a NODE_SIZE=m3.medium NUM_NODES=2 ./cluster/kube-up.sh
```

Which will deploy a 1 master 2 minion kubernetes cluster of m3.medium instances in us-west-2a. You can view the status of the cluster deployment on AWS.

## Autoscaling a Kubernetes Cluster
Currently, autoscaling can only be performed in the AWS console. Go to EC2 -> Autoscaling Groups and select the kubernetes autoscaling group. Hit Actions -> Edit and change the number of nodes to your desired node count.

## Deploying a Couchbase master
As an example, we will use the `cluster-master-podcast.yml` and `cluster-worker-podcast.yml` files as our Couchbase configuration files. A Couchbase cluster on kubernetes consists of 1 Couchbase master replication controllers, and any number of worker replication controllers.

To deploy the master node, run `./cluster/kubectl.sh create -f cluster-master-podcast.yml`. You should get the following messages back
```
replicationcontroller "couchbase-master-rc" created
service "couchbase-master-service" created
```

You can use the following commands to check the status of the deployment:
```
./cluster/kubectl.sh get svc
./cluster/kubectl.sh get po
./cluster/kubectl.sh get rc
```

Which will get the status of services, pods, and replication controllers respectively. You can also get additional information about the service using describe, for example
```
./cluster/kubectl.sh describe svc
```
Which will return something like
```
couchbase-master-podcast-service
Name:			couchbase-master-podcast-service
Namespace:		default
Labels:			app=couchbase-master-podcast-service
Selector:		app=couchbase-master-podcast-pod
Type:			LoadBalancer
IP:			10.0.215.213
LoadBalancer Ingress:	a3a0672a5043d11e7ae440601bf6be1c-1487269672.us-west-2.elb.amazonaws.com
Port:			port-8091	8091/TCP
NodePort:		port-8091	30178/TCP
Endpoints:		10.244.0.10:8091
Port:			port-8092	8092/TCP
NodePort:		port-8092	32705/TCP
Endpoints:		10.244.0.10:8092
Port:			port-8093	8093/TCP
NodePort:		port-8093	31441/TCP
Endpoints:		10.244.0.10:8093
Port:			port-8094	8094/TCP
NodePort:		port-8094	31833/TCP
Endpoints:		10.244.0.10:8094
Port:			port-11207	11207/TCP
NodePort:		port-11207	32512/TCP
Endpoints:		10.244.0.10:11207
Port:			port-11211	11211/TCP
NodePort:		port-11211	32701/TCP
Endpoints:		10.244.0.10:11211
Port:			port-11210	11210/TCP
NodePort:		port-11210	30164/TCP
Endpoints:		10.244.0.10:11210
Port:			port-18091	18091/TCP
NodePort:		port-18091	32208/TCP
Endpoints:		10.244.0.10:18091
Port:			port-18092	18092/TCP
NodePort:		port-18092	31569/TCP
Endpoints:		10.244.0.10:18092
Port:			port-18093	18093/TCP
NodePort:		port-18093	30324/TCP
Endpoints:		10.244.0.10:18093
Session Affinity:	None
Events:
  FirstSeen	LastSeen	Count	From			SubobjectPath	Type		Reason			Message
  ---------	--------	-----	----			-------------	--------	------			-------
  28m		28m		1	{service-controller }			Normal		UpdatedLoadBalancer	Updated load balancer with new hosts
```

In the above example, the value of LoadBalancer Ingress is the address of the load balancer that routes to the Couchbase cluster. Going to your browser and typing a3a0672a5043d11e7ae440601bf6be1c-1487269672.us-west-2.elb.amazonaws.com:8091 will take you to the Couchbase cluster web interface. By default the username is `Administrator` and the password is `password`.

## Deploying Couchbase workers
Now that you have a Couchbase master up, you can deploy worker replication controllers. Simply run
```
./cluster/kubectl.sh create -f cluster-worker-podcast.yml
```

This will begin deploying workers for your Couchbase cluster. As in the Couchbase master, you can check the status of the deployment with `./cluster/kubectl.sh get rc`.

Once a cluster is deployed, navigate to the address in your LoadBalancer to get to the Couchbase web console. Under Server Nodes, you should pending rebalances. This is your new worker node trying to join the Couchbase cluster. To finish joining the nodes, hit Rebalance.

## Scaling the number of Couchbase workers
In the above example we only deployed a single worker node. To scale the number of workers, we can use the command
```
kubectl scale rc couchbase-worker-podcast-rc  --replicas=3
```
The above command will scale the number of worker replicas to 3. As above, you can use `./cluster/kubectl.sh get rc` to monitor the status of your deployment, and rebalance the nodes on the Couchbase webconsole.
