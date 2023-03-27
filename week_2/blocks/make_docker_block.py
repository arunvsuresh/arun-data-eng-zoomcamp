from prefect.infrastructure.docker import DockerContainer

# alternative to creating docker container block in orion UI
docker_container_block = DockerContainer(
    image="arunvsuresh/prefect:zoomcamp",
    image_pull_policy="ALWAYS",
    auto_remove=True
)

docker_container_block.save("zoomcamp", overwrite=True)