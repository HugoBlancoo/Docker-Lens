import docker

docker_cli = docker.from_env()

async def get_container_by_id(container_id: str):
    try:
        container = docker_cli.containers.get(container_id)
        print("Container found")
        return container
    except Exception as e:
        return{"Error {e}"}