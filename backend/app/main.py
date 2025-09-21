import docker.errors
from fastapi import FastAPI
import docker

from services.getters import get_container_by_id

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

@app.get("/containers/{container_id}/stats")
async def get_stats(container_id: str):
    try:
        container = await get_container_by_id(container_id)
        stats = container.stats(stream=False)
        return {
                "cpu_usage": stats["cpu_stats"]["cpu_usage"]["total_usage"],
                "memory_usage": stats["memory_stats"]["usage"],
                "memory_limit": stats["memory_stats"]["limit"],
                "network_rx": stats["networks"]["eth0"]["rx_bytes"] if "networks" in stats else 0,
                "network_tx": stats["networks"]["eth0"]["tx_bytes"] if "networks" in stats else 0
            }
    except (docker.errors.APIError):
        return{"Internal Error"}

@app.get("/containers/{container_id}/logs")
async def get_logs(container_id: str):
    try:
        container = await get_container_by_id(container_id)
        return container.logs()
    except (docker.errors.APIError):
        return{"Internal Error"}

@app.post("/containers/{container_id}/restart")
async def restart_container_from_id(container_id: str):
    container = await get_container_by_id(container_id)
    container.restart()
    return {"message": f"Container {container_id} restarted successfully"}
