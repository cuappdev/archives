## Pushing new iterations

For now, we're not using ECS so this is how to push:

```bash
ssh -i [pem-key] ubuntu@54.174.47.32
cd ~/devOps/tcat-docker/
sudo docker kill $(sudo docker ps -q)
sudo docker rm $(sudo docker ps -a -q)
sudo docker rmi $(sudo docker images -q)
sudo docker-compose up --force-recreate -d
```
