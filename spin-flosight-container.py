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