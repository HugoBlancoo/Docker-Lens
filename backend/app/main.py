from fastapi import FastAPI
import docker

app = FastAPI()
docker_cli = docker.from_env()

@app.get("/containers")
async def get_containers():
    containers = docker_cli.containers.list()
    container_list = []
    
    for container in containers:
        container_info = {
            "id": container.short_id,
            "name": container.name,
            "image": container.image.tags[0] if container.image.tags else container.image.id,
            "status": container.status,
            "created": container.attrs['Created'],
            "ports": container.ports
        }
        container_list.append(container_info)
    
    return {"containers": container_list}
