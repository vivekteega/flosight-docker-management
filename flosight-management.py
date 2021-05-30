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

import sys
import re
import logging
import docker 
from docker.types import Mount
client = docker.from_env()

container_list = client.containers.list()

for container in container_list:
    container_status = container.status 
    #if container_status == 'running':
    #    pass
    #elif container_status == 'exited':
    if True:
        # get its attributes before stopping
        # port number | volume name | logs 
        hostIp = container.ports['80/tcp'][0]['HostIp']
        hostPort = container.ports['80/tcp'][0]['HostPort']
        volumeName = container.attrs['Mounts'][0]['Name']

        split_volumeName = volumeName.split('_')
        container_number = 0
        
        if len(split_volumeName) == 0:
            print(f"Error : Something seems wrong in the volume name {volumeName}")
            sys.exit()
        elif len(split_volumeName) == 1:
            conntainer_number = 0
        elif len(split_volumeName) == 2:
            # Check if the end of string(the 2nd object in list) is in the format `auto<number>`
            if bool(re.search('^auto[0-9]*', split_volumeName[1])):
                # extract the number
                container_number = int(re.findall(r'\d+', 'auto123')[0])
        
        '''
        docker run -d --name=flosight \
                        -p 8080:80 \
                        --mount source=flosight,target=/data \
                        --env NETWORK=mainnet --env ADDNODE=0.0.0.0 \ --env BLOCKCHAIN_BOOTSTRAP=http://servername:port/data.tar.gz
                        ranchimallfze/flosight
        '''
        
        
        # stop the container 
        container.stop()
        print("Stopped Docker")

        # spin a new container on the next port 
        # todo - check if the port is open 
        
        ## Prepare a Docker container configurations and parameters 
        ##
        container_name = f"{split_volumeName[0]}_auto{container_number+1}"
        container_port = {'80/tcp': 8234}
        container_environment = {"NETWORK":"mainnet", "ADDNODE":"0.0.0.0", "BLOCKCHAIN_BOOTSTRAP":"http://ranchimall2.duckdns.org:2488/data.tar.gz"}
        container_mounts = [Mount(source=f"{container_name}", target='/data', type='volume')]
        container_image = 'ff6295a3700e'

        # create volume and run container 
        client.volumes.create(container_name)
        print("pre")
        client.containers.run(name=container_name, image=container_image, environment=container_environment, mounts=container_mounts, ports=container_port, detach=True)
        print("post")

        # NGINX CONFIGURATION 

        # CERTBOT CONFIGURATION 

