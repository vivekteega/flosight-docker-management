'''
name 
url 
container 
port 

'''

import sys
from tinydb import TinyDB, Query
import docker
import pdb

docker_client = docker.from_env()

if len(sys.argv) == 1:
    logging.info("\nPass the currently running flosight container's hash as first command line argument to the script\nPass full file location of flosight's nginx filen as 2nd CL argument")
    sys.exit(0)

flosight_container = sys.argv[1]
flosight_nginxfile_location = sys.argv[2]
for container in docker_client.containers.list():
    if container.id.startswith(flosight_container):
        nginxdb = TinyDB('nginx.json')
        entry = Query()
        nginxdb.insert({ 'name':f"{container.name}", 'url':'flosight.duckdns.org', 'id':f"{container.id}", 'port':f"{container.ports['80/tcp'][0]['HostPort']}", 'location':f"{flosight_nginxfile_location}"})
        nginxdb.close()
        sys.exit()
