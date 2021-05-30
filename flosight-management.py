'''
Simple Docker container Orchestration with Python 

1. Check if the container is unhealthy ( next level would be to understand when its not unhealthy but not responding) 
2. If no, exit script 
3. If yes, stop the container 
4. Spin a new container on the next port 
5. Change nginx configuration 
6. Change certbot configuration 


docker volume create flosight 

docker run -d --name=flosight \
    -p 8080:80 \
    --mount source=flosight,target=/data \
    --env NETWORK=mainnet --env ADDNODE=ranchimall1.duckdns.org \ --env BLOCKCHAIN_BOOTSTRAP=http://servername:port/data.tar.gz
    ranchimallfze/flosight

'''

import docker 
from docker.types import Mount
from tinydb import TinyDB, Query
import sys
import re
import logging

docker_client = docker.from_env()
logging.basicConfig(filename='flosight-management.log', 
                    encoding='utf-8', 
                    level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')

container_list = docker_client.containers.list()
for container in container_list:
    container_status = container.status 
    if container_status == 'running':
        pass
    elif container_status == 'exited':
        # get its attributes before stopping
        # port number | volume name | logs 
        hostIp = container.ports['80/tcp'][0]['HostIp']
        hostPort = container.ports['80/tcp'][0]['HostPort']
        volumeName = container.attrs['Mounts'][0]['Name']

        split_volumeName = volumeName.split('_')
        container_number = 0
        
        if len(split_volumeName) == 0:
            logging.info(f"Error : Something seems wrong in the volume name {volumeName}")
            sys.exit()
        elif len(split_volumeName) == 1:
            conntainer_number = 0
        elif len(split_volumeName) == 2:
            # Check if the end of string(the 2nd object in list) is in the format `auto<number>`
            if bool(re.search('^auto[0-9]*', split_volumeName[1])):
                # extract the number
                container_number = int(re.findall(r'\d+', 'auto123')[0])
        
        # stop the container 
        container.stop()
        logging.info("Stopped Docker")

        # spin a new container on the next port 
        # todo - check if the port is open 
        
        ## Prepare a Docker container configurations and parameters 
        ##
        container_name = f"{split_volumeName[0]}_auto{container_number+1}"
        container_port = {'80/tcp': f"{hostPort+1}"}
        container_environment = {"NETWORK":"mainnet", "ADDNODE":"0.0.0.0", "BLOCKCHAIN_BOOTSTRAP":"http://ranchimall2.duckdns.org:2488/data.tar.gz"}
        container_mounts = [Mount(source=f"{container_name}", target='/data', type='volume')]
        container_image = 'ff6295a3700e'

        # create volume and run container 
        docker_client.volumes.create(container_name)
        logging.info("pre")
        docker_client.containers.run(name=container_name, image=container_image, environment=container_environment, mounts=container_mounts, ports=container_port, detach=True)
        logging.info("post")

        # NGINX CONFIGURATION 
        ## update nginx file of Flosight's url  
        nginxdb = TinyDB('nginx.json')
        entry = Query()
        flosight_entry= nginxdb.search(entry.url=='flosight.duckdns.org')
        flosight_entry = flosight_entry[0]

        ## check if the current container is the right one 
        if flosight_entry.id.startswith(container.id):
            # change the nginx configuration for this docker container 
            
            

        # CERTBOT CONFIGURATION 

