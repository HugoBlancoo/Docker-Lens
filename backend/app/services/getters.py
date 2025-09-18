import docker

docker_cli = docker.from_env()

async def get_container_by_id(container_id: str):
    container = docker_cli.containers.get(container_id)
    return container