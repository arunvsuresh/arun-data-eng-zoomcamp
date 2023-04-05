from prefect.deployments import Deployment
# from prefect.infrastructure.docker import DockerContainer
from etl_web_to_gcs import etl_parent_flow

# docker_block = DockerContainer.load("zoomcamp")

deployment = Deployment.build_from_flow(
    flow=etl_parent_flow,
    name='prefect-cloud-deployment',
    # infrastructure=docker_block
)

if __name__ == "__main__":
    deployment.apply()